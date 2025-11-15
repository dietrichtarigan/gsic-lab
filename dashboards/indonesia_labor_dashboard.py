from __future__ import annotations

"""Streamlit dashboard modules for Indonesia labor market intelligence."""

from pathlib import Path

import numpy as np
import pydeck as pdk

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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
    "employment_to_population_ratio": "Employment to Population Ratio",
    "employment_in_agriculture": "Employment in Agriculture",
    "employment_in_industry": "Employment in Industry",
    "employment_in_services": "Employment in Services",
    "average_working_hours_per_week": "Average Working Hours per Week",
}

BETTER_HIGHER = {
    "TPAK",
    "female_labor_participation_rate",
    "wage_growth_rate",
    "digital_skills_index",
    "employment_to_population_ratio",
    "employment_in_services",
    "average_working_hours_per_week",
}

RPJMN_TARGETS = {
    "TPT": 4.5,
    "TPAK": 71.0,
    "informal_employment_share": 55.0,
    "female_labor_participation_rate": 55.0,
    "digital_skills_index": 0.5,
}

BASE_SALARY_BY_SECTOR = {
    "Agriculture": 2800000,
    "Industry": 3800000,
    "Services": 4200000,
}

BLK_PROGRAMS = pd.DataFrame(
    [
        {
            "name": "BBPLK Bekasi",
            "province": "Jawa Barat",
            "specialization": "Manufaktur & Otomasi",
            "focus_skills": "Welding, CNC, Industrial Robotics",
            "capacity": 1200,
        },
        {
            "name": "BBPLK Serang",
            "province": "Banten",
            "specialization": "Pariwisata & Hospitality",
            "focus_skills": "Front Office, F&B Service, Housekeeping",
            "capacity": 950,
        },
        {
            "name": "BBPLK Makassar",
            "province": "Sulawesi Selatan",
            "specialization": "Maritime & Logistik",
            "focus_skills": "Port Management, Welding, Electrical",
            "capacity": 780,
        },
        {
            "name": "BBPLK Medan",
            "province": "Sumatera Utara",
            "specialization": "Digital & Kreatif",
            "focus_skills": "Data Analytics, UI/UX, Digital Marketing",
            "capacity": 880,
        },
        {
            "name": "BBPLK Jayapura",
            "province": "Papua",
            "specialization": "Pertanian Berkelanjutan",
            "focus_skills": "Agri-Tech, Hydroponics, Cold Chain",
            "capacity": 520,
        },
    ]
)

RNG = np.random.default_rng(42)

GTCI_TRENDS = {
    "Indonesia": [51.6, 52.1, 52.9, 53.7, 54.4, 55.2],
    "Malaysia": [60.4, 60.9, 61.2, 61.5, 62.0, 62.4],
    "Thailand": [58.1, 58.0, 58.3, 58.8, 59.5, 60.1],
    "Philippines": [54.2, 54.5, 54.8, 55.0, 55.3, 55.6],
    "Singapore": [73.4, 73.8, 74.1, 74.6, 75.0, 75.5],
    "Vietnam": [55.0, 55.3, 55.8, 56.4, 57.1, 57.9],
}
GTCI_YEARS = list(range(2019, 2025))
GTCI_TIME_SERIES = pd.DataFrame(
    [
        {"year": year, "country": country, "score": scores[idx]}
        for country, scores in GTCI_TRENDS.items()
        for idx, year in enumerate(GTCI_YEARS)
    ]
)
GTCI_PILLARS_INDONESIA = {
    "Enable": 49.2,
    "Attract": 45.5,
    "Grow": 60.1,
    "Retain": 48.7,
    "VT Skills": 58.3,
    "Global Knowledge": 51.5,
}
GTCI_PILLAR_INSIGHTS = {
    "Enable": "Memperkuat institusi pasar tenaga kerja, reformasi perizinan, dan digitalisasi layanan publik.",
    "Attract": "Tarik investasi SDM, buka jalur talent visa, dan kembangkan insentif untuk sektor bernilai tambah.",
    "Grow": "Percepat re-skilling dan kemitraan industri-universitas untuk mendongkrak produktivitas.",
    "Retain": "Perbaiki sistem proteksi sosial, fleksibilitas kerja, dan benefit lintas sektor.",
    "VT Skills": "Skalakan sertifikasi vokasi, BLK 4.0, dan link & match dengan kebutuhan industri.",
    "Global Knowledge": "Dorong R&D, adopsi teknologi frontier, dan kolaborasi riset dengan global tech hubs.",
}
GTCI_WEIGHTS = {
    "Enable": 0.16,
    "Attract": 0.18,
    "Grow": 0.18,
    "Retain": 0.14,
    "VT Skills": 0.17,
    "Global Knowledge": 0.17,
}
GTCI_PEER_BASE = {
    country: scores[-1] for country, scores in GTCI_TRENDS.items()
}
GTCI_PILLAR_BREAKDOWN = {
    "Enable": pd.DataFrame(
        [
            {"Komponen": "Institusi Pasar Kerja", "Nilai": 56},
            {"Komponen": "Regulasi Bisnis", "Nilai": 49},
            {"Komponen": "Adopsi Digital Pemerintah", "Nilai": 42},
        ]
    ),
    "Attract": pd.DataFrame(
        [
            {"Komponen": "FDI Human Capital", "Nilai": 44},
            {"Komponen": "Talent Visa", "Nilai": 32},
            {"Komponen": "Inklusi Tenaga Kerja", "Nilai": 47},
        ]
    ),
    "Grow": pd.DataFrame(
        [
            {"Komponen": "Universitas Top 500", "Nilai": 58},
            {"Komponen": "Lifelong Learning", "Nilai": 64},
            {"Komponen": "Kemitraan Industri", "Nilai": 63},
        ]
    ),
    "Retain": pd.DataFrame(
        [
            {"Komponen": "Proteksi Sosial", "Nilai": 46},
            {"Komponen": "Kesehatan & Wellbeing", "Nilai": 52},
            {"Komponen": "Fleksibilitas Kerja", "Nilai": 48},
        ]
    ),
    "VT Skills": pd.DataFrame(
        [
            {"Komponen": "Sertifikasi Vokasi", "Nilai": 55},
            {"Komponen": "Output BLK", "Nilai": 61},
            {"Komponen": "SMK-Industry Link", "Nilai": 59},
        ]
    ),
    "Global Knowledge": pd.DataFrame(
        [
            {"Komponen": "R&D Spending", "Nilai": 48},
            {"Komponen": "Ekspor High-Tech", "Nilai": 52},
            {"Komponen": "Global Innovation Link", "Nilai": 54},
        ]
    ),
}

DIGITAL_READINESS_DATA = pd.DataFrame(
    [
        {
            "province": "DKI Jakarta",
            "latitude": -6.2,
            "longitude": 106.82,
            "imdi_infrastructure": 86,
            "imdi_empowerment": 78,
            "imdi_job": 74,
            "digital_literacy": 82,
            "pillar_skills": 80,
            "pillar_ethics": 76,
            "pillar_culture": 84,
            "pillar_safety": 75,
        },
        {
            "province": "Banten",
            "latitude": -6.12,
            "longitude": 106.15,
            "imdi_infrastructure": 74,
            "imdi_empowerment": 63,
            "imdi_job": 58,
            "digital_literacy": 60,
            "pillar_skills": 59,
            "pillar_ethics": 55,
            "pillar_culture": 61,
            "pillar_safety": 54,
        },
        {
            "province": "DI Yogyakarta",
            "latitude": -7.8,
            "longitude": 110.37,
            "imdi_infrastructure": 69,
            "imdi_empowerment": 81,
            "imdi_job": 65,
            "digital_literacy": 78,
            "pillar_skills": 79,
            "pillar_ethics": 74,
            "pillar_culture": 83,
            "pillar_safety": 72,
        },
        {
            "province": "Jawa Barat",
            "latitude": -6.9,
            "longitude": 107.6,
            "imdi_infrastructure": 71,
            "imdi_empowerment": 68,
            "imdi_job": 61,
            "digital_literacy": 62,
            "pillar_skills": 63,
            "pillar_ethics": 58,
            "pillar_culture": 65,
            "pillar_safety": 57,
        },
        {
            "province": "Jawa Tengah",
            "latitude": -7.15,
            "longitude": 110.14,
            "imdi_infrastructure": 66,
            "imdi_empowerment": 59,
            "imdi_job": 52,
            "digital_literacy": 55,
            "pillar_skills": 54,
            "pillar_ethics": 50,
            "pillar_culture": 58,
            "pillar_safety": 51,
        },
        {
            "province": "Bali",
            "latitude": -8.34,
            "longitude": 115.09,
            "imdi_infrastructure": 73,
            "imdi_empowerment": 76,
            "imdi_job": 72,
            "digital_literacy": 77,
            "pillar_skills": 75,
            "pillar_ethics": 73,
            "pillar_culture": 82,
            "pillar_safety": 74,
        },
        {
            "province": "Sulawesi Selatan",
            "latitude": -5.15,
            "longitude": 119.41,
            "imdi_infrastructure": 62,
            "imdi_empowerment": 58,
            "imdi_job": 55,
            "digital_literacy": 53,
            "pillar_skills": 52,
            "pillar_ethics": 49,
            "pillar_culture": 55,
            "pillar_safety": 48,
        },
        {
            "province": "Papua",
            "latitude": -2.53,
            "longitude": 140.71,
            "imdi_infrastructure": 45,
            "imdi_empowerment": 38,
            "imdi_job": 32,
            "digital_literacy": 36,
            "pillar_skills": 34,
            "pillar_ethics": 30,
            "pillar_culture": 37,
            "pillar_safety": 28,
        },
        {
            "province": "Kalimantan Timur",
            "latitude": -0.51,
            "longitude": 117.15,
            "imdi_infrastructure": 68,
            "imdi_empowerment": 64,
            "imdi_job": 69,
            "digital_literacy": 58,
            "pillar_skills": 57,
            "pillar_ethics": 53,
            "pillar_culture": 61,
            "pillar_safety": 52,
        },
        {
            "province": "Nusa Tenggara Timur",
            "latitude": -8.65,
            "longitude": 121.08,
            "imdi_infrastructure": 51,
            "imdi_empowerment": 46,
            "imdi_job": 40,
            "digital_literacy": 44,
            "pillar_skills": 42,
            "pillar_ethics": 39,
            "pillar_culture": 47,
            "pillar_safety": 38,
        },
    ]
)

VACANCY_DATES = pd.date_range("2024-01-01", periods=18, freq="MS")
SECTORS = ["Manufaktur", "Digital", "Pariwisata", "Konstruksi"]
VACANCY_TRENDS = pd.DataFrame(
    [
        {
            "date": date,
            "sector": sector,
            "vacancies": (
                200 + 20 * idx + RNG.normal(0, 10)
                + {
                    "Manufaktur": 40,
                    "Digital": 80,
                    "Pariwisata": 30,
                    "Konstruksi": 55,
                }[sector]
            )
            * (1 + (0.02 * i if sector == "Digital" else 0.01 * i))
        }
        for i, date in enumerate(VACANCY_DATES)
        for idx, sector in enumerate(SECTORS)
    ]
)
VACANCY_TRENDS["vacancies"] = VACANCY_TRENDS["vacancies"].clip(lower=50)
LAYOFF_TRENDS = pd.DataFrame(
    [
        {
            "date": date,
            "sector": sector,
            "layoffs": (
                80 + 10 * idx + np.random.normal(0, 5)
                + {"Manufaktur": 20, "Digital": 5, "Pariwisata": 25, "Konstruksi": 15}[sector]
            )
            * (1 + (0.015 * i if sector == "Pariwisata" else 0.0))
        }
        for i, date in enumerate(VACANCY_DATES)
        for idx, sector in enumerate(SECTORS)
    ]
)
LAYOFF_TRENDS["layoffs"] = LAYOFF_TRENDS["layoffs"].clip(lower=10)

SKILL_DEMAND_SNAPSHOT = pd.DataFrame(
    [
        {"skill": "Python", "share": 12.4, "mom_change": 2.5},
        {"skill": "SQL", "share": 10.1, "mom_change": 1.9},
        {"skill": "Data Visualization", "share": 9.5, "mom_change": 2.1},
        {"skill": "Project Management", "share": 8.8, "mom_change": 1.3},
        {"skill": "AutoCAD", "share": 7.1, "mom_change": 1.7},
        {"skill": "Welding", "share": 6.4, "mom_change": 1.1},
        {"skill": "Digital Marketing", "share": 5.9, "mom_change": 2.9},
        {"skill": "Green Logistics", "share": 4.7, "mom_change": 3.4},
    ]
)

EMERGING_SKILL_TRENDS = pd.DataFrame(
    [
        {"month": date, "skill": skill, "growth_index": base + 3 * i}
        for i, date in enumerate(pd.date_range("2024-01-01", periods=8, freq="MS"))
        for skill, base in {
            "AI Safety": 40,
            "Sustainability Reporting": 35,
            "Robotics Maintenance": 42,
        }.items()
    ]
)

VOCATIONAL_MISMATCH = {
    "Teknik Informatika": {
        "curriculum": ["C Programming", "Database", "Networking", "UI/UX"],
        "demand": {"Python": 1200, "SQL": 1050, "Cybersecurity": 900, "Cloud": 850},
    },
    "Teknik Mesin": {
        "curriculum": ["CAD Dasar", "Termodinamika", "Pemeliharaan Mesin"],
        "demand": {"AutoCAD": 980, "CNC": 920, "Predictive Maintenance": 740},
    },
    "Hospitality": {
        "curriculum": ["Front Office", "Housekeeping", "F&B Service"],
        "demand": {"Revenue Management": 620, "Digital Guest Experience": 560, "Barista Specialty": 510},
    },
    "Logistik": {
        "curriculum": ["Warehouse", "Transport Planning", "Customs"],
        "demand": {"Green Logistics": 690, "ERP": 630, "Cold Chain": 580},
    },
}

DECENT_WORK_BENCHMARK = {
    "Produktivitas": {
        "Indonesia": 28700,
        "Malaysia": 39800,
        "Thailand": 32300,
        "Vietnam": 21900,
    },
    "Wage_Salaried": {
        "Indonesia": 45.6,
        "Malaysia": 65.2,
        "Thailand": 52.3,
        "Vietnam": 40.8,
    },
    "Female_LFP": {
        "Indonesia": 56.6,
        "Malaysia": 55.2,
        "Thailand": 61.0,
        "Vietnam": 62.5,
    },
    "Informal_Wage_Penalty": {
        "Indonesia": 36.0,
        "Malaysia": 18.0,
        "Thailand": 24.0,
        "Vietnam": 29.0,
    },
}


def _normalize(values: pd.Series) -> pd.Series:
    """Scale data between 0 and 1; used for relative scoring."""

    min_val = values.min()
    max_val = values.max()
    if max_val == min_val:
        return pd.Series(0.5, index=values.index)
    return (values - min_val) / (max_val - min_val)


@st.cache_data(show_spinner=False)
def load_data(path: Path | str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame["year"] = frame["year"].astype(int)
    frame["semester"] = frame["semester"].astype(int)
    frame["period_order"] = (frame["year"] - frame["year"].min()) * 2 + (frame["semester"] - 1)
    frame["period_label"] = frame["year"].astype(str) + ":" + frame["semester"].map({1: "Feb", 2: "Aug"})
    frame["period_date"] = pd.to_datetime(
        frame["year"].astype(str) + frame["semester"].map({1: "-02-01", 2: "-08-01"})
    )
    frame["employment_to_population_ratio"] = frame.get("employment_to_population_ratio", frame["TPAK"] * 0.95)
    return frame


def compute_national(frame: pd.DataFrame) -> pd.DataFrame:
    metrics = {
        "TPAK": "mean",
        "TPT": "mean",
        "informal_employment_share": "mean",
        "underemployment_rate": "mean",
        "youth_NEET_rate": "mean",
        "wage_growth_rate": "mean",
        "digital_skills_index": "mean",
        "female_labor_participation_rate": "mean",
        "employment_in_agriculture": "mean",
        "employment_in_industry": "mean",
        "employment_in_services": "mean",
    }
    agg = (
        frame.groupby(["period_order", "period_date", "period_label"], as_index=False)
        .agg(metrics)
        .sort_values("period_order")
    )
    return agg


def compute_supply_demand_profiles(frame: pd.DataFrame) -> pd.DataFrame:
    latest_period = frame["period_order"].max()
    snapshot = frame[frame["period_order"] == latest_period]
    cols = [
        "TPAK",
        "TPT",
        "underemployment_rate",
        "wage_growth_rate",
        "digital_skills_index",
        "female_labor_participation_rate",
        "informal_employment_share",
        "employment_in_agriculture",
        "employment_in_industry",
        "employment_in_services",
    ]
    profile = snapshot[["province", *cols]].set_index("province")
    supply_index = (
        0.4 * _normalize(profile["TPAK"]) +
        0.3 * _normalize(profile["female_labor_participation_rate"]) +
        0.3 * (1 - _normalize(profile["underemployment_rate"]))
    )
    demand_index = (
        0.4 * (1 - _normalize(profile["TPT"])) +
        0.3 * _normalize(profile["wage_growth_rate"]) +
        0.3 * _normalize(profile["digital_skills_index"])
    )
    mismatch = demand_index - supply_index
    profile = profile.assign(
        supply_index=supply_index,
        demand_index=demand_index,
        mismatch_gap=mismatch,
    ).reset_index()
    return profile


def highlight_delta(current: float, reference: float) -> str:
    delta = current - reference
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.2f} pp"


def render_macro_overview(data: pd.DataFrame, national: pd.DataFrame) -> None:
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

    st.markdown("### National Trajectory")
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

    st.markdown("### Provincial Recovery Leaders and Laggards")
    latest_period = data.loc[data["period_order"].idxmax(), "period_order"]
    latest_snapshot = data[data["period_order"] == latest_period]
    indicator_choice = st.selectbox(
        "Pilih indikator untuk peringkat provinsi",
        list(INDICATOR_LABELS.keys()),
        format_func=lambda key: INDICATOR_LABELS[key],
        key="macro_indicator_ranking",
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

    st.markdown("### Province Explorer")
    provinces = sorted(data["province"].unique().tolist())
    default_selection = ["DKI Jakarta", "Banten", "Bali", "Nusa Tenggara Timur"]
    selected = st.multiselect("Pilih provinsi untuk dibandingkan", provinces, default=default_selection)
    indicator_explorer = st.selectbox(
        "Pilih indikator waktu", [key for key in INDICATOR_LABELS.keys() if key not in {
            "employment_in_agriculture",
            "employment_in_industry",
            "employment_in_services",
        }],
        format_func=lambda key: INDICATOR_LABELS[key],
        key="macro_indicator_explorer",
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
        "Sumber: Dataset sintetis Sakernas 2020-2023 (Labor Market Intelligence & Policy Lab)."
    )


def project_gtci_score(improvements: dict[str, float]) -> tuple[float, int, pd.DataFrame]:
    baseline = GTCI_PEER_BASE["Indonesia"]
    weighted_delta = sum(GTCI_WEIGHTS[pillar] * improvements.get(pillar, 0.0) for pillar in GTCI_WEIGHTS)
    projected_score = baseline + 0.6 * weighted_delta
    peer_scores = {country: score for country, score in GTCI_PEER_BASE.items()}
    peer_scores["Indonesia"] = projected_score
    ranking = (
        pd.Series(peer_scores, name="Score")
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"index": "Country"})
    )
    indonesia_positions = ranking.index[ranking["Country"] == "Indonesia"]
    if indonesia_positions.empty:
        rank_position = len(ranking)
    else:
        rank_position = int(indonesia_positions[0]) + 1
    return projected_score, rank_position, ranking


def render_talent_competitiveness_module() -> None:
    st.markdown("### Talent Competitiveness Control Tower")
    st.write(
        "Benchmark posisi Indonesia dalam persaingan talent regional, dekonstruksi pilar GTCI, dan simulasikan tuas kebijakan untuk mengejar ketertinggalan."
    )

    leaderboard_fig = px.bar(
        GTCI_TIME_SERIES,
        x="score",
        y="country",
        color="country",
        animation_frame="year",
        range_x=[45, 80],
        orientation="h",
        title="ASEAN Talent War Leaderboard (2019-2024)",
        labels={"score": "Skor GTCI", "country": "Negara"},
    )
    leaderboard_fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(leaderboard_fig, use_container_width=True)

    st.markdown("#### GTCI Pillar Control Panel")
    gauge_rows = [st.columns(3), st.columns(3)]
    latest_score = GTCI_PEER_BASE["Indonesia"]
    for idx, (pillar, value) in enumerate(GTCI_PILLARS_INDONESIA.items()):
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#10a37f"},
                    "threshold": {"line": {"color": "#ff4b4b", "width": 3}, "value": 65},
                },
                title={"text": pillar},
            )
        )
        container = gauge_rows[idx // 3][idx % 3]
        container.plotly_chart(fig, use_container_width=True)

    selected_pillar = st.radio(
        "Pilih pilar untuk melihat dekonstruksi detail",
        list(GTCI_PILLARS_INDONESIA.keys()),
        horizontal=True,
        key="gtci_pillar_select",
    )
    st.info(GTCI_PILLAR_INSIGHTS[selected_pillar])
    st.dataframe(GTCI_PILLAR_BREAKDOWN[selected_pillar].set_index("Komponen"))

    st.markdown("#### Policy Lever Simulator")
    st.write(
        "Eksplorasi dampak peningkatan skor pilar terhadap proyeksi skor GTCI Indonesia. Rentang slider merepresentasikan kenaikan poin skor pilar."
    )
    slider_columns = st.columns(3)
    improvements: dict[str, float] = {}
    for idx, pillar in enumerate(GTCI_PILLARS_INDONESIA.keys()):
        improvements[pillar] = slider_columns[idx % 3].slider(
            pillar,
            min_value=-3.0,
            max_value=20.0,
            value=0.0,
            step=0.5,
            key=f"gtci_slider_{pillar}",
        )

    projected_score, projected_rank, ranking = project_gtci_score(improvements)
    st.metric(
        "Projected GTCI Score",
        f"{projected_score:.1f}",
        f"{projected_score - latest_score:+.1f}",
    )
    st.metric("Projected ASEAN Rank", f"#{projected_rank}")
    st.dataframe(ranking.set_index("Country"))


def render_digital_readiness_module() -> None:
    st.markdown("### Digital Readiness & Mismatch Map")
    st.write(
        "Integrasi skor IMDI, literasi digital SMERU, dan kesiapan kerja untuk memetakan mismatch infrastruktur vs skill."
    )

    map_df = DIGITAL_READINESS_DATA.copy()
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position="[longitude, latitude]",
        get_radius="(imdi_infrastructure + imdi_empowerment) * 1200",
        get_fill_color="[imdi_infrastructure * 2, (100 - digital_literacy) * 2, 160]",
        pickable=True,
    )
    tooltip = {
        "html": "<b>{province}</b><br/>IMDI Infrastruktur: {imdi_infrastructure}<br/>Literasi Digital: {digital_literacy}",
        "style": {"backgroundColor": "#0e1117", "color": "white"},
    }
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=pdk.ViewState(latitude=-2.5, longitude=118.0, zoom=3.7, pitch=35),
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        tooltip=tooltip,
    )
    st.pydeck_chart(deck)

    wired_unskilled = map_df[(map_df["imdi_infrastructure"] >= 70) & (map_df["digital_literacy"] <= 60)]
    skilled_unwired = map_df[(map_df["imdi_infrastructure"] <= 60) & (map_df["digital_literacy"] >= 70)]
    col_a, col_b = st.columns(2)
    col_a.markdown("**Wired but Unskilled**")
    if wired_unskilled.empty:
        col_a.write("Tidak ada provinsi dengan mismatch ini.")
    else:
        col_a.table(wired_unskilled[["province", "imdi_infrastructure", "digital_literacy"]].set_index("province"))
    col_b.markdown("**Skilled but Unwired**")
    if skilled_unwired.empty:
        col_b.write("Tidak ada provinsi dengan mismatch ini.")
    else:
        col_b.table(skilled_unwired[["province", "imdi_infrastructure", "digital_literacy"]].set_index("province"))

    scatter_fig = px.scatter(
        map_df,
        x="imdi_job",
        y="imdi_empowerment",
        size="digital_literacy",
        color="province",
        text="province",
        labels={"imdi_job": "IMDI Pilar Pekerjaan", "imdi_empowerment": "IMDI Pilar Pemberdayaan"},
        title="Pemberdayaan vs Pekerjaan: Siapkah Provinsi Memanfaatkan Ekonomi Digital?",
    )
    scatter_fig.update_traces(textposition="top center")
    st.plotly_chart(scatter_fig, use_container_width=True)

    st.markdown("#### Diagnostic Radar per Provinsi")
    selected_province = st.selectbox("Pilih provinsi", map_df["province"].tolist(), key="digital_province")
    province_row = map_df.set_index("province").loc[selected_province]
    radar_df = pd.DataFrame(
        {
            "Pilar": ["Skills", "Ethics", "Culture", "Safety"],
            "Nilai": [
                province_row["pillar_skills"],
                province_row["pillar_ethics"],
                province_row["pillar_culture"],
                province_row["pillar_safety"],
            ],
        }
    )
    national_avg = map_df[["pillar_skills", "pillar_ethics", "pillar_culture", "pillar_safety"]].mean()
    radar_df_avg = pd.DataFrame(
        {
            "Pilar": ["Skills", "Ethics", "Culture", "Safety"],
            "Nilai": [
                national_avg["pillar_skills"],
                national_avg["pillar_ethics"],
                national_avg["pillar_culture"],
                national_avg["pillar_safety"],
            ],
            "Series": "Rata-rata Nasional",
        }
    )
    radar_df_selected = radar_df.assign(Series=selected_province)
    radar_fig = px.line_polar(
        pd.concat([radar_df_selected, radar_df_avg]),
        r="Nilai",
        theta="Pilar",
        color="Series",
        line_close=True,
        title=f"Pilar Literasi Digital: {selected_province} vs Nasional",
    )
    st.plotly_chart(radar_fig, use_container_width=True)


def render_real_time_demand_module() -> None:
    st.markdown("### Real-Time Demand & Decent Work Tracker")
    st.write(
        "Pantau dinamika lowongan kerja, pulse PHK, skill yang sedang panas, serta scorecard Decent Work dibandingkan ASEAN."
    )

    vacancy_total = VACANCY_TRENDS.groupby("date", as_index=False)["vacancies"].sum().rename(columns={"vacancies": "Job Vacancies"})
    layoff_total = LAYOFF_TRENDS.groupby("date", as_index=False)["layoffs"].sum().rename(columns={"layoffs": "Layoff Reports"})
    tracker = vacancy_total.merge(layoff_total, on="date", how="left")
    ews_fig = go.Figure()
    ews_fig.add_trace(
        go.Scatter(x=tracker["date"], y=tracker["Job Vacancies"], mode="lines+markers", name="Lowongan Baru")
    )
    ews_fig.add_trace(
        go.Scatter(x=tracker["date"], y=tracker["Layoff Reports"], mode="lines+markers", name="Laporan PHK", yaxis="y2")
    )
    ews_fig.update_layout(
        title="Early Warning Pulse: Lowongan vs PHK",
        xaxis_title="Periode",
        yaxis=dict(title="Indeks Lowongan"),
        yaxis2=dict(title="Laporan PHK", overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.15, x=0.02),
    )
    st.plotly_chart(ews_fig, use_container_width=True)

    sector_fig = px.line(
        VACANCY_TRENDS,
        x="date",
        y="vacancies",
        color="sector",
        markers=True,
        title="Lowongan Baru per Sektor",
        labels={"date": "Periode", "vacancies": "Jumlah Lowongan", "sector": "Sektor"},
    )
    st.plotly_chart(sector_fig, use_container_width=True)

    st.markdown("#### Skill Genome Snapshot (30 Hari Terakhir)")
    skills_fig = px.bar(
        SKILL_DEMAND_SNAPSHOT.sort_values("mom_change", ascending=False),
        x="skill",
        y="share",
        color="mom_change",
        labels={"skill": "Skill", "share": "% Lowongan", "mom_change": "Δ MoM (pp)"},
        title="Demand Share & Momentum",
    )
    st.plotly_chart(skills_fig, use_container_width=True)

    emerging_fig = px.line(
        EMERGING_SKILL_TRENDS,
        x="month",
        y="growth_index",
        color="skill",
        markers=True,
        title="Top Emerging Skills Momentum",
        labels={"month": "Periode", "growth_index": "Indeks Pertumbuhan", "skill": "Skill"},
    )
    st.plotly_chart(emerging_fig, use_container_width=True)

    st.markdown("#### Mismatch Calculator")
    program_choice = st.selectbox("Pilih program vokasi", list(VOCATIONAL_MISMATCH.keys()), key="mismatch_program")
    selected_program = VOCATIONAL_MISMATCH[program_choice]
    curriculum_df = pd.DataFrame(selected_program["curriculum"], columns=["Kurikulum Saat Ini"])
    demand_df = (
        pd.Series(selected_program["demand"], name="Jumlah Lowongan")
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"index": "Skill yang Dicari"})
    )
    col_cur, col_gap = st.columns(2)
    col_cur.write("Kurikulum")
    col_cur.table(curriculum_df)
    col_gap.write("Permintaan Industri")
    col_gap.table(demand_df)

    st.markdown("#### Decent Work & Productivity Scorecard")
    prod = DECENT_WORK_BENCHMARK["Produktivitas"]
    wage = DECENT_WORK_BENCHMARK["Wage_Salaried"]
    female = DECENT_WORK_BENCHMARK["Female_LFP"]
    penalty = DECENT_WORK_BENCHMARK["Informal_Wage_Penalty"]
    metric_cols = st.columns(3)
    metric_cols[0].metric(
        "Produktivitas (GDP/Pekerja) 🇮🇩",
        f"US$ {prod['Indonesia']:,.0f}",
        f"vs 🇲🇾 US$ {prod['Malaysia']:,.0f}",
    )
    metric_cols[1].metric(
        "Wage & Salaried Workers 🇮🇩",
        f"{wage['Indonesia']:.1f}%",
        f"vs ASEAN Leader 🇲🇾 {wage['Malaysia']:.1f}%",
    )
    metric_cols[2].metric(
        "TPAK Perempuan 🇮🇩",
        f"{female['Indonesia']:.1f}%",
        f"vs 🇹🇭 {female['Thailand']:.1f}%",
    )
    st.metric(
        "Informal Wage Penalty 🇮🇩",
        f"{penalty['Indonesia']:.0f}%",
        f"ASEAN Avg ≈ {np.mean([penalty['Malaysia'], penalty['Thailand'], penalty['Vietnam']]):.0f}%",
    )

def render_supply_demand_module(data: pd.DataFrame) -> None:
    st.markdown("### Supply-Demand Intelligence & Skill Mismatch")
    profiles = compute_supply_demand_profiles(data)
    national_supply = profiles["supply_index"].mean()
    national_demand = profiles["demand_index"].mean()
    col_supply, col_demand = st.columns(2)
    col_supply.metric("Indeks Supply Nasional", f"{national_supply:.2f}")
    col_demand.metric("Indeks Demand Nasional", f"{national_demand:.2f}")

    gap_ordered = profiles.sort_values("mismatch_gap", ascending=False)
    st.plotly_chart(
        px.bar(
            gap_ordered,
            x="province",
            y="mismatch_gap",
            title="Provinsi dengan Gap Demand-Supply terbesar",
            labels={"province": "Provinsi", "mismatch_gap": "Gap (Demand - Supply)"},
        ).update_layout(xaxis_tickangle=-40),
        use_container_width=True,
    )

    top_focus = gap_ordered.head(8)["province"].tolist()
    bottom_focus = gap_ordered.tail(8)["province"].tolist()
    sector_focus = data[data["province"].isin(top_focus + bottom_focus)]
    sector_pivot = (
        sector_focus.groupby("province")[
            ["employment_in_agriculture", "employment_in_industry", "employment_in_services"]
        ].mean()
    )
    heat_fig = px.imshow(
        sector_pivot.sort_values("employment_in_industry", ascending=False),
        color_continuous_scale="Blues",
        title="Struktur Ketenagakerjaan: Fokus Provinsi Prioritas",
        labels=dict(color="Persentase Pekerja (%)"),
    )
    st.plotly_chart(heat_fig, use_container_width=True)

    st.markdown("#### Analisis Skill yang Dicari vs Pasokan")
    selected_province = st.selectbox("Pilih provinsi", profiles["province"].tolist(), key="skill_gap_province")
    province_profile = profiles.set_index("province").loc[selected_province]
    spillover = pd.DataFrame(
        {
            "Komponen": [
                "TPAK",
                "Partisipasi Kerja Perempuan",
                "Underemployment (dibalik)",
                "Wage Growth",
                "Digital Skills",
            ],
            "Indeks": [
                province_profile["TPAK"],
                province_profile["female_labor_participation_rate"],
                100 - province_profile["underemployment_rate"],
                province_profile["wage_growth_rate"],
                province_profile["digital_skills_index"] * 100,
            ],
        }
    )
    radar_fig = px.line_polar(
        spillover,
        r="Indeks",
        theta="Komponen",
        line_close=True,
        title=f"Komposisi Supply-Demand {selected_province}",
    )
    st.plotly_chart(radar_fig, use_container_width=True)


def render_regional_benchmarking_module(data: pd.DataFrame, national: pd.DataFrame) -> None:
    st.markdown("### Regional Benchmarking & Peer Learning")
    provinces = sorted(data["province"].unique())
    default_selection = ["Jawa Barat", "Banten", "DKI Jakarta"]
    selected = st.multiselect(
        "Bandingkan provinsi",
        provinces,
        default=[prov for prov in default_selection if prov in provinces],
        key="regional_compare",
    )
    if not selected:
        st.info("Pilih minimal satu provinsi untuk analisis benchmarking.")
        return

    latest_order = data["period_order"].max()
    latest_snapshot = data[data["period_order"] == latest_order]
    compare_cols = [
        "TPAK",
        "TPT",
        "informal_employment_share",
        "underemployment_rate",
        "wage_growth_rate",
        "digital_skills_index",
    ]
    comparison = latest_snapshot[latest_snapshot["province"].isin(selected)][["province", *compare_cols]]
    comparison_long = comparison.melt(id_vars="province", var_name="Indikator", value_name="Nilai")
    comparison_long["Label"] = comparison_long["Indikator"].map(INDICATOR_LABELS)
    st.plotly_chart(
        px.bar(
            comparison_long,
            x="Label",
            y="Nilai",
            color="province",
            barmode="group",
            title="Perbandingan KPI Utama",
        ).update_layout(xaxis_tickangle=-30),
        use_container_width=True,
    )

    st.markdown("#### Trajektori Jangka Menengah")
    horizon_indicator = st.selectbox(
        "Pilih indikator", ["TPAK", "TPT", "informal_employment_share", "digital_skills_index"],
        format_func=lambda key: INDICATOR_LABELS[key],
        key="regional_indicator_trend",
    )
    regional_trend = data[data["province"].isin(selected)]
    st.plotly_chart(
        px.line(
            regional_trend,
            x="period_date",
            y=horizon_indicator,
            color="province",
            markers=True,
            labels={"period_date": "Period", horizon_indicator: INDICATOR_LABELS[horizon_indicator]},
            title=f"Trajektori {INDICATOR_LABELS[horizon_indicator]}",
        ),
        use_container_width=True,
    )

    national_latest = national.iloc[-1]
    scorecards = comparison.copy()
    for col in compare_cols:
        scorecards[f"Delta {col}"] = scorecards[col] - national_latest[col]
    st.markdown("#### Provincial Scorecard vs Rata-rata Nasional")
    st.dataframe(scorecards.set_index("province"))


def render_ews_module(data: pd.DataFrame, national: pd.DataFrame) -> None:
    st.markdown("### Early Warning System & Leading Indicators")
    latest_order = data["period_order"].max()
    prev_order = latest_order - 1
    latest_snapshot = data[data["period_order"] == latest_order]
    prev_snapshot = data[data["period_order"] == prev_order]

    if prev_snapshot.empty:
        st.info("Belum ada histori cukup untuk EWS.")
        return

    merged = latest_snapshot.merge(prev_snapshot, on="province", suffixes=("_latest", "_prev"))
    merged["tpt_change"] = merged["TPT_latest"] - merged["TPT_prev"]
    merged["underemployment_change"] = (
        merged["underemployment_rate_latest"] - merged["underemployment_rate_prev"]
    )
    merged["wage_pulse"] = merged["wage_growth_rate_latest"] - merged["wage_growth_rate_prev"]

    alert_threshold = st.slider("Ambang peringatan TPT (pp)", 0.5, 3.0, 1.0, step=0.1)
    alerts = merged[merged["tpt_change"] >= alert_threshold].sort_values("tpt_change", ascending=False)
    if alerts.empty:
        st.success("Tidak ada lonjakan TPT di atas ambang saat ini.")
    else:
        st.error("Provinsi dengan lonjakan TPT signifikan:")
        st.dataframe(
            alerts[["province", "TPT_prev", "TPT_latest", "tpt_change", "underemployment_rate_latest"]].rename(
                columns={
                    "province": "Provinsi",
                    "TPT_prev": "TPT Sebelumnya",
                    "TPT_latest": "TPT Terkini",
                    "tpt_change": "Perubahan (pp)",
                    "underemployment_rate_latest": "Underemployment %",
                }
            ).set_index("Provinsi")
        )

    st.markdown("#### Leading Indicator Pulse")
    pulse = merged[["province", "wage_pulse", "digital_skills_index_latest", "underemployment_change"]]
    pulse = pulse.rename(
        columns={
            "wage_pulse": "Momentum Upah",
            "digital_skills_index_latest": "Indeks Digital",
            "underemployment_change": "Perubahan Underemployment",
        }
    )
    st.dataframe(pulse.set_index("province"))

    national_latest = national.iloc[-1]
    national_prev = national.iloc[-2]
    vacancy_index = 100 + (national_latest["wage_growth_rate"] - national_prev["wage_growth_rate"]) * 5
    st.metric("SiapKerja Job Vacancy Index (proxy)", f"{vacancy_index:.1f}")
    st.caption("Proxy berbasis tren pertumbuhan upah. Integrasikan data JOLTS/SiapKerja untuk indeks riil.")


def render_policy_tracker_module(national: pd.DataFrame) -> None:
    st.markdown("### Policy Lab & RPJMN Tracker")
    latest_row = national.iloc[-1]
    prev_row = national.iloc[0]
    cols = st.columns(len(RPJMN_TARGETS))
    for idx, (indicator, target) in enumerate(RPJMN_TARGETS.items()):
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=float(latest_row[indicator]),
                delta={"reference": float(prev_row[indicator])},
                gauge={
                    "axis": {"range": [None, max(target * 1.2, float(latest_row[indicator]) * 1.1 + 1)]},
                    "threshold": {"value": target, "line": {"color": "red", "width": 3}},
                },
                title={"text": INDICATOR_LABELS.get(indicator, indicator)},
            )
        )
        cols[idx].plotly_chart(fig, use_container_width=True)

    st.markdown("#### Benchmark Internasional")
    benchmark_data = pd.DataFrame(
        [
            {"negara": "Indonesia", "Produktivitas": 1.0, "Partisipasi Perempuan": latest_row["female_labor_participation_rate"], "Digital Skills": latest_row["digital_skills_index"]},
            {"negara": "Malaysia", "Produktivitas": 1.15, "Partisipasi Perempuan": 55.0, "Digital Skills": 0.58},
            {"negara": "Vietnam", "Produktivitas": 0.95, "Partisipasi Perempuan": 62.0, "Digital Skills": 0.45},
            {"negara": "Thailand", "Produktivitas": 1.05, "Partisipasi Perempuan": 60.0, "Digital Skills": 0.5},
            {"negara": "Singapura", "Produktivitas": 1.45, "Partisipasi Perempuan": 64.0, "Digital Skills": 0.72},
        ]
    )
    st.plotly_chart(
        px.scatter(
            benchmark_data,
            x="Produktivitas",
            y="Partisipasi Perempuan",
            size="Digital Skills",
            color="negara",
            title="ASEAN/G20 Benchmark: Produktivitas vs Partisipasi Perempuan",
            labels={"Produktivitas": "Produktivitas Relatif", "Partisipasi Perempuan": "%"},
        ),
        use_container_width=True,
    )


def estimate_salary(province_row: pd.Series, sector: str, experience_years: float) -> float:
    base = BASE_SALARY_BY_SECTOR[sector]
    wage_growth = province_row.get("wage_growth_rate", 0) / 100
    underemployment_penalty = max(0.0, (province_row.get("underemployment_rate", 0) - 5) / 100)
    experience_premium = 0.03 * experience_years
    estimate = base * (1 + wage_growth) * (1 + experience_premium) * (1 - 0.5 * underemployment_penalty)
    return round(estimate, -2)


def render_training_module(data: pd.DataFrame) -> None:
    st.markdown("### Pelatihan, BLK, dan Citizen Tools")
    provinces = sorted(BLK_PROGRAMS["province"].unique())
    province_filter = st.multiselect("Filter provinsi", provinces)
    specialization_filter = st.text_input("Cari spesialisasi atau skill")

    filtered = BLK_PROGRAMS.copy()
    if province_filter:
        filtered = filtered[filtered["province"].isin(province_filter)]
    if specialization_filter:
        filtered = filtered[filtered["focus_skills"].str.contains(specialization_filter, case=False)]

    st.dataframe(filtered.set_index("name"))

    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Unduh Direktori BLK (CSV)", csv_data, file_name="blk_directory.csv", mime="text/csv")

    st.markdown("#### Kalkulator Estimasi Gaji")
    latest_order = data["period_order"].max()
    latest_snapshot = data[data["period_order"] == latest_order].set_index("province")
    province_choice = st.selectbox("Provinsi", sorted(latest_snapshot.index.tolist()), key="salary_province")
    sector_choice = st.selectbox("Sektor", list(BASE_SALARY_BY_SECTOR.keys()), key="salary_sector")
    experience_years = st.slider("Pengalaman (tahun)", 0, 20, 2)
    province_row = latest_snapshot.loc[province_choice]
    estimated_salary = estimate_salary(province_row, sector_choice, experience_years)
    st.success(
        f"Estimasi gaji bulanan untuk {sector_choice} di {province_choice} dengan pengalaman {experience_years} tahun: Rp {estimated_salary:,.0f}"
    )


def main() -> None:
    st.set_page_config(page_title="Indonesia Labor Market Intelligence", layout="wide")
    st.title("Indonesia Labor Market Intelligence Dashboard")
    st.write(
        "Sistem intelijen pasar tenaga kerja terintegrasi untuk Labor Market Intelligence & Policy Lab. "
        "Jelajahi modul-modul untuk memahami dinamika supply-demand, benchmarking regional, early warning, dan dukungan kebijakan."
    )

    data = load_data(DATA_PATH)
    national = compute_national(data)

    tabs = st.tabs([
        "Talent Control Tower",
        "Digital Readiness Map",
        "Real-Time Demand",
        "Macro Overview",
        "Supply-Demand & Skill Gap",
        "Regional Benchmarking",
        "Early Warning System",
        "Policy Lab",
        "Pelatihan & Citizen Tools",
    ])

    with tabs[0]:
        render_talent_competitiveness_module()
    with tabs[1]:
        render_digital_readiness_module()
    with tabs[2]:
        render_real_time_demand_module()
    with tabs[3]:
        render_macro_overview(data, national)
    with tabs[4]:
        render_supply_demand_module(data)
    with tabs[5]:
        render_regional_benchmarking_module(data, national)
    with tabs[6]:
        render_ews_module(data, national)
    with tabs[7]:
        render_policy_tracker_module(national)
    with tabs[8]:
        render_training_module(data)


if __name__ == "__main__":
    main()
