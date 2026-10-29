"""Lab 17: a FRED/ALFRED point-in-time rates viewer.

Run: streamlit run asof_app.py
"""

from datetime import date
from io import StringIO

import altair as alt
import pandas as pd
import requests
import streamlit as st

FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
ALFRED_URL = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
DEFAULT_SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}


def display_date(value):
    stamp = pd.Timestamp(value)
    return f"{stamp:%B} {stamp.day}, {stamp.year}"


def read_series_csv(text, series_id):
    """Parse FRED/ALFRED CSV data and remove FRED's '.' missing values."""
    raw = pd.read_csv(StringIO(text), na_values=".")
    date_column = next(
        (name for name in raw.columns if name.lower() in {"date", "observation_date"}), None
    )
    if raw.empty or date_column is None:
        raise ValueError("FRED did not return a usable DATE column.")
    value_column = series_id.upper() if series_id.upper() in raw.columns else None
    if value_column is None:
        values = [name for name in raw.columns if name != date_column]
        if len(values) != 1:
            raise ValueError("FRED did not return a usable value column.")
        value_column = values[0]
    data = raw[[date_column, value_column]].rename(
        columns={date_column: "DATE", value_column: "value"}
    )
    data["DATE"] = pd.to_datetime(data["DATE"], errors="coerce")
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    return data.dropna().sort_values("DATE").reset_index(drop=True)


@st.cache_data(ttl=3600, show_spinner=False)
def download_today(series_id):
    """One FRED request for the current version of a series."""
    response = requests.get(FRED_URL, params={"id": series_id}, timeout=30)
    response.raise_for_status()
    return read_series_csv(response.text, series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_as_known_on(series_id, vintage_date):
    """One ALFRED request for the version available on a specified date."""
    response = requests.get(
        ALFRED_URL, params={"id": series_id, "vintage_date": vintage_date}, timeout=30
    )
    response.raise_for_status()
    return read_series_csv(response.text, series_id)


def audit_row(series_id, vintage, current):
    known_last = vintage.iloc[-1]
    current_last = current.iloc[-1]
    known_date = pd.Timestamp(known_last["DATE"])
    shared = vintage.merge(current, on="DATE", suffixes=("_then", "_today"))
    return {
        "Series ID": f"https://fred.stlouisfed.org/series/{series_id}",
        "Last date known then": known_date.date(),
        "Value known then": float(known_last["value"]),
        "Last date measured today": pd.Timestamp(current_last["DATE"]).date(),
        "Value today": float(current_last["value"]),
        "Today's values after then": int((current["DATE"] > known_date).sum()),
        "Revised shared dates": int((shared["value_then"] != shared["value_today"]).sum()),
    }


def comparison_chart(frames, chart_type):
    wide = pd.concat(frames, ignore_index=True).pivot(
        index="DATE", columns="series_id", values="value"
    )
    long = wide.rename_axis("DATE").reset_index().melt(
        id_vars="DATE", var_name="Series", value_name="Value"
    ).dropna()
    order = list(wide.columns)
    colors = alt.Scale(domain=order, scheme="tableau10")
    if chart_type == "Line chart":
        chart = alt.Chart(long).mark_line(point=True).encode(
            x=alt.X("DATE:T", title="Date"),
            y=alt.Y("Value:Q", title="Rate / value"),
            color=alt.Color("Series:N", scale=colors, legend=alt.Legend(title="Series")),
            tooltip=["DATE:T", "Series:N", alt.Tooltip("Value:Q", format=".3f")],
        )
    else:
        # One bar per series/month prevents daily DGS10 values forming a solid band.
        bars = long.assign(Month=long["DATE"].dt.to_period("M")).sort_values("DATE")
        bars = bars.groupby(["Month", "Series"], as_index=False).last()
        bars["Month"] = bars["Month"].dt.to_timestamp()
        bars["Month label"] = bars["Month"].astype(str)
        chart = alt.Chart(bars).mark_bar().encode(
            x=alt.X(
                "Month label:N", title="Month (last available observation)",
                sort=alt.EncodingSortField(field="Month", order="ascending"),
            ),
            xOffset=alt.XOffset("Series:N", sort=order),
            y=alt.Y("Value:Q", title="Rate / value"),
            color=alt.Color("Series:N", scale=colors, legend=alt.Legend(title="Series")),
            tooltip=["Month label:N", "Series:N", alt.Tooltip("Value:Q", format=".3f")],
        )
    return chart.properties(height=420).interactive()


def main():
    st.set_page_config(page_title="Point-in-Time Rates", layout="wide")
    st.title("Point-in-Time Rates")
    st.caption(
        "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, "
        f"downloaded {display_date(date.today())}; built with AI help, a learning "
        "demonstration, not investment advice."
    )

    st.sidebar.header("Controls")
    selected = st.sidebar.multiselect(
        "Series IDs", list(DEFAULT_SERIES), default=list(DEFAULT_SERIES),
        format_func=lambda series: f"{series} - {DEFAULT_SERIES[series]}",
    )
    extra = st.sidebar.text_input("Add another FRED series ID", placeholder="Example: PAYEMS")
    if extra.strip():
        selected.append(extra.strip().upper())
    selected = list(dict.fromkeys(selected))
    start_date = st.sidebar.date_input("Start date", date(2020, 1, 1))
    as_known_on = st.sidebar.date_input("As known on", date.today())
    chart_type = st.sidebar.selectbox("Combined comparison chart", ["Line chart", "Bar chart"])

    if not selected:
        st.info("Select a series or add a FRED series ID in the sidebar.")
        return

    rows, frames = [], []
    for series_id in selected:
        try:
            current = download_today(series_id)
            vintage = download_as_known_on(series_id, as_known_on.isoformat())
            current_from_start = current[current["DATE"].dt.date >= start_date]
            title = DEFAULT_SERIES.get(series_id, series_id)
            st.subheader(f"{series_id} - {title}" if series_id in DEFAULT_SERIES else title)
            if current_from_start.empty:
                st.warning(f"{series_id}: no observations on or after {start_date}.")
            else:
                st.line_chart(current_from_start.set_index("DATE")["value"], use_container_width=True)
                frames.append(current_from_start.assign(series_id=series_id))
            known_last = vintage.iloc[-1]
            st.caption(
                f"Last date in data known on {display_date(as_known_on)}: "
                f"{display_date(known_last['DATE'])} - {known_last['value']:,.3f}"
            )
            rows.append(audit_row(series_id, vintage, current))
        except (requests.RequestException, ValueError, pd.errors.ParserError, IndexError) as error:
            st.error(f"{series_id}: {error}")

    if rows:
        st.subheader("Point-in-time audit")
        st.dataframe(
            pd.DataFrame(rows), hide_index=True, use_container_width=True,
            column_config={
                "Series ID": st.column_config.LinkColumn("Series ID", display_text=r".*/series/(.*)$"),
                "Value known then": st.column_config.NumberColumn(format="%.3f"),
                "Value today": st.column_config.NumberColumn(format="%.3f"),
            },
        )
    if frames:
        st.subheader("Combined rate comparison")
        st.caption(
            "All successfully downloaded selected series from the start date. "
            "The bar chart uses each series' last available observation each month."
        )
        st.altair_chart(comparison_chart(frames, chart_type), use_container_width=True)


if __name__ == "__main__":
    main()
