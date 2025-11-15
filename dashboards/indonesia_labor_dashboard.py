from __future__ import annotations

from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "indonesia_labor_market.csv"
INDICATOR_LABELS = {
    "TPAK": "Labor Force Participation Rate (TPAK)",
    "TPT": "Open Unemployment Rate (TPT)",
    "informal_employment_share": "Informal Employment Share",
    "underemployment_rate": "Underemployment Rate",
    "youth_NEET_rate": "Youth NEET Rate",
    "female_labor_participation_rate": "Female Labor Participation",
    "wage_growth_rate": "Wage Growth Rate",
    "education_mismatch_index": "Education Mismatch Index",
    "digital_skills_index": "Digital Skills Index",
}

BETTER_HIGHER = {
    "TPAK",
    "female_labor_participation_rate",
    "wage_growth_rate",
    "digital_skills_index",
}


@st.cache_data
def load_data(path: Path | str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame["year"] = frame["year"].astype(int)
    frame["semester"] = frame["semester"].astype(int)
    frame["period_order"] = (frame["year"] - frame["year"].min()) * 2 + (frame["semester"] - 1)
    frame["period_label"] = frame["year"].astype(str) + ":" + frame["semester"].map({1: "Feb", 2: "Aug"})
    frame["period_date"] = pd.to_datetime(
        frame["year"].astype(str) + frame["semester"].map({1: "-02-01", 2: "-08-01"})
    )
    return frame


def compute_national(frame: pd.DataFrame) -> pd.DataFrame:
    agg = (
        frame.groupby(["period_order", "period_date", "period_label"], as_index=False)
        .agg({
            "TPAK": "mean",
            "TPT": "mean",
            "informal_employment_share": "mean",
            "underemployment_rate": "mean",
            "youth_NEET_rate": "mean",
        })
        .sort_values("period_order")
    )
    return agg


def highlight_delta(current: float, reference: float) -> str:
    delta = current - reference
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.2f} pp"


def main() -> None:
    st.set_page_config(page_title="Indonesia Labor Market Intelligence", layout="wide")
    st.title("Indonesia Labor Market Intelligence Dashboard")
    st.write(
        "Synthetic Sakernas-style panel covering 34 provinces across 2020-2023. "
        "Use the controls below to explore structural pressures behind the job-full yet quality-poor recovery."
    )

    data = load_data(DATA_PATH)
    national = compute_national(data)
    peak_tpt_row = national.loc[national["TPT"].idxmax()]
    latest_row = national.iloc[-1]
    pre_pandemic_row = national.iloc[0]

    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric(
        "TPT Nasional", f"{latest_row['TPT']:.2f}%", highlight_delta(latest_row["TPT"], peak_tpt_row["TPT"])
    )
    col_b.metric(
        "TPAK Nasional", f"{latest_row['TPAK']:.2f}%", highlight_delta(latest_row["TPAK"], pre_pandemic_row["TPAK"])
    )
    col_c.metric(
        "Underemployment", f"{latest_row['underemployment_rate']:.2f}%",
        highlight_delta(latest_row["underemployment_rate"], pre_pandemic_row["underemployment_rate"]),
    )
    col_d.metric(
        "Informality", f"{latest_row['informal_employment_share']:.2f}%",
        highlight_delta(latest_row["informal_employment_share"], pre_pandemic_row["informal_employment_share"]),
    )

    st.subheader("National Trajectory")
    trend_fig = px.line(
        national,
        x="period_date",
        y="TPT",
        markers=True,
        title="Open Unemployment Rate: Pandemic Shock and Recovery",
        labels={"period_date": "Period", "TPT": "TPT (%)"},
    )
    trend_fig.add_scatter(
        x=national["period_date"],
        y=national["TPAK"],
        mode="lines+markers",
        name="TPAK",
        yaxis="y2",
    )
    trend_fig.update_layout(
        yaxis=dict(title="TPT (%)"),
        yaxis2=dict(title="TPAK (%)", overlaying="y", side="right", showgrid=False),
        legend=dict(orientation="h", y=1.15, x=0.02),
    )
    st.plotly_chart(trend_fig, use_container_width=True)

    dual_fig = px.line(
        national,
        x="period_date",
        y=["TPT", "underemployment_rate"],
        markers=True,
        labels={"value": "Rate (%)", "variable": "Indicator", "period_date": "Period"},
        title="Headline Recovery vs. Underemployment Slack",
    )
    st.plotly_chart(dual_fig, use_container_width=True)

    st.subheader("Provincial Recovery Leaders and Laggards")
    latest_period = data.loc[data["period_order"].idxmax(), "period_order"]
    latest_snapshot = data[data["period_order"] == latest_period]
    indicator_choice = st.selectbox(
        "Pilih indikator untuk peringkat provinsi",
        list(INDICATOR_LABELS.keys()),
        format_func=lambda key: INDICATOR_LABELS[key],
    )
    ascending_best = indicator_choice not in BETTER_HIGHER
    ranking = latest_snapshot.sort_values(indicator_choice, ascending=ascending_best)
    top5 = ranking.head(5)
    bottom5 = ranking.tail(5).sort_values(indicator_choice, ascending=not ascending_best)
    col_left, col_right = st.columns(2)
    col_left.write("Top 5 (Terbaik)")
    col_left.dataframe(top5[["province", indicator_choice]].set_index("province"))
    col_right.write("Bottom 5 (Terburuk)")
    col_right.dataframe(bottom5[["province", indicator_choice]].set_index("province"))
    bar_fig = px.bar(
        ranking.head(15),
        x="province",
        y=indicator_choice,
        title=f"15 Provinsi Terbaik berdasarkan {INDICATOR_LABELS[indicator_choice]}",
        labels={indicator_choice: INDICATOR_LABELS[indicator_choice], "province": "Provinsi"},
    )
    bar_fig.update_layout(xaxis_tickangle=-40)
    st.plotly_chart(bar_fig, use_container_width=True)

    st.subheader("Province Explorer")
    provinces = sorted(data["province"].unique().tolist())
    default_selection = ["DKI Jakarta", "Banten", "Bali", "Nusa Tenggara Timur"]
    selected = st.multiselect("Pilih provinsi untuk dibandingkan", provinces, default=default_selection)
    indicator_explorer = st.selectbox(
        "Pilih indikator waktu", list(INDICATOR_LABELS.keys()),
        format_func=lambda key: INDICATOR_LABELS[key], key="explorer_indicator"
    )
    filtered = data[data["province"].isin(selected)] if selected else data
    explorer_fig = px.line(
        filtered,
        x="period_date",
        y=indicator_explorer,
        color="province",
        markers=True,
        labels={"period_date": "Period", indicator_explorer: INDICATOR_LABELS[indicator_explorer]},
        title=f"{INDICATOR_LABELS[indicator_explorer]} menurut Provinsi",
    )
    st.plotly_chart(explorer_fig, use_container_width=True)

    st.caption(
        "Sumber: PDF 'Indonesian Labor Market Data Simulation' (synthetic), diekstrak otomatis dari Tabel 1."
    )


if __name__ == "__main__":
    main()
