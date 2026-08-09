"""Interactive Spain Top 50 music intelligence dashboard.

Run from the project root with: streamlit run app.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
PAGE_OPTIONS = ["Overview", "Analytics", "Research Insights", "Visualizations", "Data Explorer"]

st.set_page_config(page_title="Spain Top 50 Music Analysis", page_icon=" ", layout="wide")


@st.cache_data(show_spinner="Loading playlist intelligence ")
def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the prepared project outputs once per data-file change."""
    clean = pd.read_csv(OUTPUT_DIR / "clean_spain_top50.csv", parse_dates=["date"])
    lifecycle = pd.read_csv(OUTPUT_DIR / "song_lifecycle.csv", parse_dates=["entry_date", "exit_date"])
    churn = pd.read_csv(OUTPUT_DIR / "playlist_churn_analysis.csv", parse_dates=["date"])
    research = pd.read_csv(OUTPUT_DIR / "research_summary.csv")
    clean["is_explicit"] = clean["is_explicit"].astype(str).str.lower().eq("true")
    return clean, lifecycle, churn, research


def inject_css() -> None:
    st.markdown(
        """
        <style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f6f8fc 0%, #ffffff 55%, #eef4ff 100%);
}

.block-container {
    max-width: 1450px;
    padding-top: 2.4rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #152b52 !important;
    font-weight: 750 !important;
    letter-spacing: -0.35px;
}

h2 {
    margin-top: 1.25rem !important;
}

div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #ffffff, #f0f5ff);
    border: 1px solid #d7e4fb;
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 7px 20px rgba(26, 63, 124, 0.09);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 11px 26px rgba(26, 63, 124, 0.15);
}

div[data-testid="stMetricLabel"] {
    color: #5a6a85 !important;
    font-size: 0.83rem !important;
    font-weight: 700 !important;
}

div[data-testid="stMetricValue"] {
    color: #173d76 !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

div[data-testid="stAlert"] {
    border: 0;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(31, 59, 115, 0.07);
}

div[data-testid="stDataFrame"] {
    border: 1px solid #dbe5f3;
    border-radius: 12px;
    overflow: hidden;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #112b52 0%, #19417a 52%, #2863d6 100%);
    border-right: 1px solid rgba(255, 255, 255, 0.12);
}

section[data-testid="stSidebar"] * {
    color: #ffffff;
}

section[data-testid="stSidebar"] h2 {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.18);
}

section[data-testid="stSidebar"] label {
    font-size: 0.83rem !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-radius: 8px;
    padding: 5px 7px;
    transition: background 0.15s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.13);
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div,
section[data-testid="stSidebar"] [data-baseweb="input"] > div {
    background: #ffffff !important;
    border-radius: 9px !important;
    border: 1px solid rgba(255, 255, 255, 0.45) !important;
}

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #163b73, #2563eb);
    color: #ffffff;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 7px 16px rgba(37, 99, 235, 0.22);
}

@media (max-width: 768px) {
    .block-container {
        padding: 1.2rem 1rem 2rem;
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.55rem !important;
    }
}
</style>
        """,
        unsafe_allow_html=True,
    )
def sidebar(clean: pd.DataFrame, lifecycle: pd.DataFrame) -> tuple[str, dict]:
    with st.sidebar:
        st.markdown(
            """
            <style>
            section[data-testid="stSidebar"] input {
                background: white !important;
                color: #0F172A !important;
                -webkit-text-fill-color: #0F172A !important;
            }
            section[data-testid="stSidebar"] [data-baseweb="select"] span {
                color: #0F172A !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="padding:16px 12px 8px;text-align:center">
              <h2 style="color:white;margin:0">Spain Top 50</h2>
              <p style="font-size:13px;margin:6px 0 0">Music Intelligence Dashboard</p>
              <hr><p style="font-size:12px">Atlantic Recording Corporation</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        page = st.radio(
            "Dashboard sections",
            PAGE_OPTIONS,
            label_visibility="collapsed",
        )

        st.divider()
        st.markdown("### Filters")

        min_date = clean["date"].min().date()
        max_date = clean["date"].max().date()

        date_mode = st.selectbox(
            "Quick date range",
            [
                "All available data",
                "Last 7 days",
                "Last 30 days",
                "Last 3 months",
                "Last 6 months",
                "Last 12 months",
                "Custom date range",
            ],
        )

        max_timestamp = pd.Timestamp(max_date)

        if date_mode == "All available data":
            start_date = pd.Timestamp(min_date)
            end_date = max_timestamp

        elif date_mode == "Last 7 days":
            start_date = max(pd.Timestamp(min_date), max_timestamp - pd.Timedelta(days=6))
            end_date = max_timestamp

        elif date_mode == "Last 30 days":
            start_date = max(pd.Timestamp(min_date), max_timestamp - pd.Timedelta(days=29))
            end_date = max_timestamp

        elif date_mode == "Last 3 months":
            start_date = max(pd.Timestamp(min_date), max_timestamp - pd.DateOffset(months=3))
            end_date = max_timestamp

        elif date_mode == "Last 6 months":
            start_date = max(pd.Timestamp(min_date), max_timestamp - pd.DateOffset(months=6))
            end_date = max_timestamp

        elif date_mode == "Last 12 months":
            start_date = max(pd.Timestamp(min_date), max_timestamp - pd.DateOffset(months=12))
            end_date = max_timestamp

        else:
            selected_dates = st.date_input(
                "Select custom date range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )
            selected = list(selected_dates) if isinstance(selected_dates, (tuple, list)) else [selected_dates]
            start_date = pd.Timestamp(selected[0])
            end_date = pd.Timestamp(selected[1]) if len(selected) > 1 and selected[1] else start_date

        stages = sorted(lifecycle["stage"].dropna().unique().tolist())
        album_types = sorted(clean["album_type"].dropna().unique().tolist())

        st.markdown("**Lifecycle stage**")
        selected_stages = [stage for stage in stages if st.checkbox(stage, value=True, key=f"stage_{stage}")]
        st.markdown("**Album type**")
        selected_albums = [album_type for album_type in album_types if st.checkbox(album_type.title(), value=True, key=f"album_{album_type}")]


        content_filter = st.radio(
            "Explicit content",
            ["All", "Explicit only", "Clean only"],
            horizontal=True,
        )

        song_search = st.text_input(
            "Search song or artist",
            placeholder="Type a song or artist name",
        )

        filters = {
            "start_date": start_date,
            "end_date": end_date,
            "stages": selected_stages,
            "album_types": selected_albums,
            "content": content_filter,
            "search": song_search,
        }

        st.caption("Filters apply automatically to KPIs, charts, tables, and downloads.")

    return page, filters




def filter_data(clean: pd.DataFrame, lifecycle: pd.DataFrame, churn: pd.DataFrame, filters: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    filtered_clean = clean.loc[clean["date"].between(filters["start_date"], filters["end_date"])].copy()
    filtered_clean = filtered_clean[filtered_clean["album_type"].isin(filters["album_types"])]
    if filters["content"] == "Explicit only":
        filtered_clean = filtered_clean[filtered_clean["is_explicit"]]
    elif filters["content"] == "Clean only":
        filtered_clean = filtered_clean[~filtered_clean["is_explicit"]]
    if filters["search"]:
        term = filters["search"].strip()
        mask = filtered_clean["song"].str.contains(term, case=False, na=False) | filtered_clean["artist"].str.contains(term, case=False, na=False)
        filtered_clean = filtered_clean[mask]

    song_keys = filtered_clean[["song", "artist"]].drop_duplicates()
    filtered_lifecycle = lifecycle.merge(song_keys, on=["song", "artist"], how="inner")
    filtered_lifecycle = filtered_lifecycle[
        filtered_lifecycle["entry_date"].le(filters["end_date"])
        & filtered_lifecycle["exit_date"].ge(filters["start_date"])
        & filtered_lifecycle["stage"].isin(filters["stages"])
    ].copy()
    filtered_churn = churn.loc[churn["date"].between(filters["start_date"], filters["end_date"])].copy()
    return filtered_clean, filtered_lifecycle, filtered_churn


def calculate_kpis(clean: pd.DataFrame, lifecycle: pd.DataFrame, churn: pd.DataFrame) -> dict[str, float | int]:
    return {
        "songs": int(clean[["song", "artist"]].drop_duplicates().shape[0]),
        "lifetime": float(lifecycle["total_days"].mean()) if not lifecycle.empty else 0.0,
       "evergreen": int((lifecycle["content_maturity"].str.contains("Evergreen", case=False, na=False)).sum()),
        "churn": float(churn["churn_rate"].mean()) if not churn.empty else 0.0,
    }

def render_header() -> None:
    st.markdown(
        """
        <div style="background:linear-gradient(90deg,#183153,#2563EB);padding:25px;border-radius:18px;color:white;margin-bottom:20px;box-shadow:0 8px 20px rgba(0,0,0,.15)">
          <div style="font-size:34px;font-weight:900;color:#FFD166">  Spain Top 50 Music Analysis Dashboard</div>
          <p style="font-size:17px;margin:10px 0 0">Content Maturity   Release Lifecycle   Playlist Rotation Analysis</p>
          <p style="font-size:13px;margin-bottom:0">Atlantic Recording Corporation</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis(kpis: dict[str, float | int]) -> None:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("  Total songs", f"{kpis['songs']:,}")
    c2.metric("  Avg lifetime", f"{kpis['lifetime']:.1f} days")
    c3.metric("  Evergreen songs", f"{kpis['evergreen']:,}")
    c4.metric("  Avg churn rate", f"{kpis['churn']:.1f}%")


def empty_state() -> bool:
    st.warning("No records match the selected filters. Adjust the filters and try again.")
    return True


def render_overview(clean: pd.DataFrame, lifecycle: pd.DataFrame, churn: pd.DataFrame) -> None:
    st.header("  Business Background")
    st.info("Spain's music market is shaped by strong Latin and regional genres, sensitivity to new releases, and fast playlist rotation. This dashboard helps Atlantic Recording Corporation use those patterns to plan releases, marketing, and catalog strategy.")
    st.header("  Project Objectives")
    left, right = st.columns(2)
    left.success("  Release timing optimization\n\n  Marketing planning\n\n  Catalog vs fresh-release balance")
    right.success("  Playlist rotation strategy\n\n  Lifecycle intelligence\n\n  Content retention analysis")
    st.header("  Live Dataset Overview")
    render_kpis(calculate_kpis(clean, lifecycle, churn))
    st.caption("KPIs reflect the active date, lifecycle, album, explicit-content, and search filters.")


def render_analytics(clean: pd.DataFrame, lifecycle: pd.DataFrame, churn: pd.DataFrame) -> None:
    st.header("  Analytics")
    render_kpis(calculate_kpis(clean, lifecycle, churn))
    if lifecycle.empty:
        empty_state()
        return
    left, right = st.columns(2)
    with left:
        stage_counts = lifecycle["stage"].value_counts().rename_axis("stage").reset_index(name="songs")
        fig = px.bar(stage_counts, x="stage", y="songs", color="stage", title="Lifecycle Stage Distribution", text_auto=True)
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Songs")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        maturity = lifecycle.groupby("content_maturity", dropna=False).agg(songs=("song", "count"), avg_lifetime=("total_days", "mean")).reset_index()
        fig = px.bar(maturity, x="content_maturity", y="avg_lifetime", color="content_maturity", hover_data=["songs"], title="Content Maturity Comparison")
        fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Average lifetime (days)")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Playlist Churn Analytics")
    if churn.empty:
        empty_state()
    else:
        fig = px.line(churn, x="date", y="churn_rate", markers=True, hover_data=["entries", "exits", "playlist_status"], title="Playlist Churn Rate Over Time")
        fig.update_layout(xaxis_title=None, yaxis_title="Churn rate (%)")
        st.plotly_chart(fig, use_container_width=True)


def render_research(clean: pd.DataFrame, lifecycle: pd.DataFrame, churn: pd.DataFrame) -> None:
    st.header("  Research Insights")
    kpis = calculate_kpis(clean, lifecycle, churn)
    if lifecycle.empty:
        empty_state()
        return
    peak = lifecycle["time_to_peak"].mean()
    mature_share = (lifecycle["stage"].str.contains("Mature|Evergreen", case=False, regex=True, na=False).mean() * 100)
    c1, c2 = st.columns(2)
    c1.success(f"  Selected songs stay in the playlist for **{kpis['lifetime']:.1f} days** on average.")
    c1.success(f"  **{kpis['evergreen']:,}** selected songs are classified as evergreen.")
    c2.info(f"  Songs reach peak position in **{peak:.1f} days** on average.")
    c2.info(f"  **{mature_share:.1f}%** of selected songs are in mature or evergreen stages.")
    st.subheader("Executive Summary")
    st.markdown("The live dashboard combines playlist observations with song lifecycle outcomes. Use the controls in the sidebar to compare release formats, content maturity, and playlist turnover for the selected reporting period. The results support timing, promotional, and catalog-balance decisions for the Spanish market.")


def render_visualizations(lifecycle: pd.DataFrame, churn: pd.DataFrame) -> None:
    st.header("  Interactive Visualizations")
    if lifecycle.empty:
        empty_state()
        return
    st.subheader("Song Lifecycle Timeline")
    timeline = lifecycle.sort_values(["entry_date", "total_days"], ascending=[False, False]).head(60).copy()
    fig = px.timeline(timeline, x_start="entry_date", x_end="exit_date", y="song", color="stage", hover_data=["artist", "total_days", "peak_position", "time_to_peak", "content_maturity"])
    fig.update_yaxes(autorange="reversed", title=None)
    fig.update_layout(height=max(450, len(timeline) * 18), legend_title="Lifecycle stage")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Entry vs Exit Flow")
    if churn.empty:
        empty_state()
    else:
        flow = churn.melt(id_vars="date", value_vars=["entries", "exits"], var_name="event", value_name="songs")
        fig = px.bar(flow, x="date", y="songs", color="event", barmode="group", title="Playlist Entries vs Exits")
        fig.update_layout(xaxis_title=None, yaxis_title="Songs")
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Song Longevity and Peak Position")
    fig = px.scatter(lifecycle, x="total_days", y="peak_position", color="stage", size="popularity" if "popularity" in lifecycle.columns else None, hover_data=["song", "artist", "content_maturity", "time_to_peak"], title="Lifecycle Duration vs Best Playlist Position")
    fig.update_yaxes(autorange="reversed", title="Peak position (1 is best)")
    fig.update_layout(xaxis_title="Lifecycle duration (days)")
    st.plotly_chart(fig, use_container_width=True)


def csv_bytes(data: pd.DataFrame) -> bytes:
    return data.to_csv(index=False).encode("utf-8")


def render_explorer(clean: pd.DataFrame, lifecycle: pd.DataFrame, churn: pd.DataFrame) -> None:
    st.header("  Interactive Data Explorer")
    if clean.empty:
        empty_state()
        return
    lifecycle_columns = ["song", "artist", "entry_date", "exit_date", "total_days", "peak_position", "time_to_peak", "stage", "content_maturity"]
    explorer = lifecycle[lifecycle_columns].sort_values(["total_days", "peak_position"], ascending=[False, True]) if not lifecycle.empty else pd.DataFrame()
    st.dataframe(explorer, use_container_width=True, hide_index=True, column_config={"entry_date": st.column_config.DateColumn("Entry date"), "exit_date": st.column_config.DateColumn("Exit date")})
    c1, c2, c3 = st.columns(3)
    c1.download_button("Download filtered playlist CSV", csv_bytes(clean), "filtered_playlist_data.csv", "text/csv", use_container_width=True)
    c2.download_button("Download lifecycle CSV", csv_bytes(explorer), "filtered_song_lifecycle.csv", "text/csv", use_container_width=True, disabled=explorer.empty)
    c3.download_button("Download churn CSV", csv_bytes(churn), "filtered_playlist_churn.csv", "text/csv", use_container_width=True, disabled=churn.empty)


def main() -> None:
    inject_css()
    try:
        clean, lifecycle, churn, _research = load_data()
    except FileNotFoundError as exc:
        st.error(f"A required prepared-data file is missing: {exc.filename}")
        st.stop()
    page, filters = sidebar(clean, lifecycle)
    filtered_clean, filtered_lifecycle, filtered_churn = filter_data(clean, lifecycle, churn, filters)
    render_header()
    if page == "Overview":
        render_overview(filtered_clean, filtered_lifecycle, filtered_churn)
    elif page == "Analytics":
        render_analytics(filtered_clean, filtered_lifecycle, filtered_churn)
    elif page == "Research Insights":
        render_research(filtered_clean, filtered_lifecycle, filtered_churn)
    elif page == "Visualizations":
        render_visualizations(filtered_lifecycle, filtered_churn)
    else:
        render_explorer(filtered_clean, filtered_lifecycle, filtered_churn)


if __name__ == "__main__":
    main()
