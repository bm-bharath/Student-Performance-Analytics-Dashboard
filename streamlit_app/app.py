import streamlit as st # pyright: ignore[reportMissingImports]
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import plotly.express as px # pyright: ignore[reportMissingImports]
from pathlib import Path


DATA_PATH = Path("../processed/student_performance_clean.csv")


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # ---- Ensure human-readable labels ----
    # If some columns got encoded as 0/1, convert them back to Yes/No or proper strings

    # Gender: 0/1 -> Male/Female (if needed)
    if df["Gender"].dtype != "O":  # not object (string)
        df["Gender"] = df["Gender"].map({0: "Male", 1: "Female"}).fillna(df["Gender"].astype(str))

    # Learning Style mapping
    learning_style_map = {
            0: "Visual",
            1: "Auditory",
            2: "Kinesthetic",
            3: "Reading/Writing"
        }

    if df["LearningStyle"].dtype != "O":
        df["LearningStyle"] = df["LearningStyle"].map(learning_style_map).fillna(df["LearningStyle"])


    # LearningStyle: if encoded somehow, keep as string
    df["LearningStyle"] = df["LearningStyle"].astype(str)

    # Generic Yes/No mapping for certain columns if numeric
    binary_cols = ["Extracurricular", "Internet", "OnlineCourses", "EduTech"]
    for col in binary_cols:
        if col in df.columns and df[col].dtype != "O":
            df[col] = df[col].map({1: "Yes", 0: "No"}).fillna("Unknown")

    return df


def add_light_minimal_theme():
    st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff;
                color: #111111;
                font-family: -apple-system, BlinkMacSystemFont, -webkit-system-font,
                             "SF Pro Text", "SF Pro Display", "Segoe UI", Roboto, Oxygen, sans-serif;
            }
            /* Remove default padding at the top to let hero breathe */
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                max-width: 1200px;
            }
            /* Hero section */
            .hero-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 2.5rem;
                padding: 1.75rem 2rem;
                border-radius: 18px;
                background: radial-gradient(circle at top left, #f5fbff, #ffffff);
                border: 1px solid #E6EAF0;
                box-shadow: 0 18px 60px rgba(15, 23, 42, 0.06);
                margin-bottom: 1.75rem;
            }
            .hero-left-title {
                font-size: 1.9rem;
                font-weight: 650;
                letter-spacing: -0.02em;
                margin-bottom: 0.5rem;
                color: #111827;
            }
            .hero-left-subtitle {
                font-size: 0.98rem;
                color: #4B5563;
                max-width: 460px;
                margin-bottom: 1rem;
            }
            .hero-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                padding: 0.30rem 0.7rem;
                border-radius: 999px;
                background: #EEF2FF;
                color: #4338CA;
                font-size: 0.78rem;
                font-weight: 500;
                margin-bottom: 0.75rem;
            }
            .hero-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 0.4rem;
                margin-top: 0.4rem;
            }
            .hero-tag {
                padding: 0.22rem 0.6rem;
                border-radius: 999px;
                background: #F3F4F6;
                font-size: 0.78rem;
                color: #4B5563;
            }
            .hero-right-card {
                flex: 0 0 340px;
                border-radius: 16px;
                background: #F9FAFB;
                border: 1px solid #E5E7EB;
                padding: 1rem 1.2rem;
            }
            .hero-right-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.8rem;
            }
            .hero-right-title {
                font-size: 0.9rem;
                font-weight: 600;
                color: #111827;
            }
            .hero-right-badge {
                font-size: 0.72rem;
                padding: 0.16rem 0.5rem;
                border-radius: 999px;
                background: #DBEAFE;
                color: #1D4ED8;
            }
            .hero-right-bars {
                display: grid;
                grid-template-columns: 1fr;
                gap: 0.3rem;
                margin-bottom: 0.8rem;
            }
            .hero-right-bar-row {
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            .hero-right-bar-label {
                font-size: 0.75rem;
                color: #6B7280;
                min-width: 90px;
            }
            .hero-right-bar-track {
                flex: 1;
                height: 6px;
                border-radius: 999px;
                background: #E5E7EB;
                overflow: hidden;
            }
            .hero-right-bar-fill {
                height: 100%;
                border-radius: 999px;
                background: linear-gradient(90deg, #38BDF8, #6366F1);
            }
            .hero-metrics-row {
                display: flex;
                gap: 0.6rem;
                margin-top: 0.4rem;
            }
            .hero-metric-chip {
                flex: 1;
                padding: 0.45rem 0.6rem;
                border-radius: 12px;
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                font-size: 0.75rem;
                color: #4B5563;
            }
            .hero-metric-label {
                font-size: 0.7rem;
                color: #9CA3AF;
            }
            .hero-metric-value {
                font-size: 0.9rem;
                font-weight: 600;
                color: #111827;
            }

            .metric-card {
                padding: 16px;
                border-radius: 12px;
                background: #F9FAFB;
                border: 1px solid #E5E7EB;
                box-shadow: none;
                margin-bottom: 10px;
            }
            .metric-card h3 {
                font-size: 0.8rem;
                color: #6B7280;
                margin-bottom: 4px;
            }
            .metric-card p {
                font-size: 1.4rem;
                font-weight: 600;
                color: #111827;
                margin: 0;
            }
            .section-title {
                font-size: 1.1rem;
                font-weight: 600;
                margin-top: 0.75rem;
                margin-bottom: 0.15rem;
                color: #111827;
            }
            .section-subtitle {
                font-size: 0.9rem;
                color: #6B7280;
                margin-bottom: 0.7rem;
            }
            hr {
                border: none;
                border-top: 1px solid #E5E7EB;
                margin-top: 1.5rem;
                margin-bottom: 1.5rem;
            }
        </style>
    """, unsafe_allow_html=True)




def metric_card(title: str, value: str):
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>{title}</h3>
            <p>{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def overview_tab(df: pd.DataFrame):
    st.markdown("### 📊 Overview – How Are Students Performing Overall?")
    st.markdown(
        "<p class='section-subtitle'>High-level summary of performance, attendance and learning styles.</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Students (Filtered)", f"{len(df):,}")
    with col2:
        metric_card("Avg Exam Score", f"{df['ExamScore'].mean():.1f}")
    with col3:
        metric_card("Avg Attendance (%)", f"{df['Attendance'].mean():.1f}")
    with col4:
        if "PerformanceCategory" in df.columns:
            high_pct = (df["PerformanceCategory"] == "High").mean() * 100
            metric_card("High Performers (%)", f"{high_pct:.1f} %")

    st.markdown("<div class='section-title'>Score Distribution</div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-subtitle'>How are exam scores spread across students?</p>",
        unsafe_allow_html=True,
    )
    fig_exam = px.histogram(
        df,
        x="ExamScore",
        nbins=30,
        title="Exam Score Distribution",
    )
    fig_exam.update_layout(template="plotly_white", bargap=0.05)
    st.plotly_chart(fig_exam, use_container_width=True)
    
    if "PerformanceCategory" in df.columns:
        st.markdown("<div class='section-title'>Performance Categories</div>", unsafe_allow_html=True)
        perf_counts = df["PerformanceCategory"].value_counts().reset_index()
        perf_counts.columns = ["PerformanceCategory", "Count"]
        fig_perf = px.bar(
            perf_counts,
            x="PerformanceCategory",
            y="Count",
            text="Count",
            title="Students by Performance Category",
        )
        fig_perf.update_traces(textposition="outside")
        fig_perf.update_layout(template="plotly_dark", xaxis_title="", yaxis_title="Number of Students")
        st.plotly_chart(fig_perf, use_container_width=True)

    st.markdown("<div class='section-title'>Learning Styles Breakdown</div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-subtitle'>Which learning preferences are most common in this group?</p>",
        unsafe_allow_html=True,
    )
    ls_counts = df["LearningStyle"].value_counts().reset_index()
    ls_counts.columns = ["LearningStyle", "Count"]
    fig_ls = px.pie(
        ls_counts,
        names="LearningStyle",
        values="Count",
        title="Learning Style Distribution",
        hole=0.4,
    )
    fig_ls.update_layout(template="plotly_dark")
    st.plotly_chart(fig_ls, use_container_width=True)


def attendance_study_tab(df: pd.DataFrame):
    st.markdown("### 🎯 Attendance & Study Habits – Where Is the Sweet Spot?")
    st.markdown(
        "<p class='section-subtitle'>Understand how attendance and study hours relate to exam performance.</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>Attendance vs Exam Score</div>", unsafe_allow_html=True)
        st.markdown(
            "<p class='section-subtitle'>Each point is a student. Higher to the right = better attendance, higher up = better score.</p>",
            unsafe_allow_html=True,
        )
        color_col = "PerformanceCategory" if "PerformanceCategory" in df.columns else None
        fig_att = px.scatter(
            df,
            x="Attendance",
            y="ExamScore",
            color=color_col,
            title="Attendance vs Exam Score",
            trendline="ols",
        )
        fig_att.update_layout(template="plotly_dark", xaxis_title="Attendance (%)", yaxis_title="Exam Score")
        st.plotly_chart(fig_att, use_container_width=True)

    with col2:
        if "AttendanceBucket" in df.columns:
            st.markdown("<div class='section-title'>Average Score by Attendance Group</div>", unsafe_allow_html=True)
            group_att = df.groupby("AttendanceBucket")["ExamScore"].mean().reset_index()
            fig_att_bucket = px.bar(
                group_att,
                x="AttendanceBucket",
                y="ExamScore",
                title="Average Exam Score by Attendance Group",
                text="ExamScore",
            )
            fig_att_bucket.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            fig_att_bucket.update_layout(
                template="plotly_dark",
                xaxis_title="Attendance Group",
                yaxis_title="Average Exam Score",
            )
            st.plotly_chart(fig_att_bucket, use_container_width=True)

    st.markdown("<div class='section-title'>Study Hours & Performance</div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-subtitle'>Compare exam scores across different weekly study-hour ranges.</p>",
        unsafe_allow_html=True,
    )
    if "StudyHoursBucket" in df.columns:
        fig_study = px.box(
            df,
            x="StudyHoursBucket",
            y="ExamScore",
            points="all",
            title="Exam Score by Study Hours Group",
        )
        fig_study.update_layout(
            template="plotly_dark",
            xaxis_title="Study Hours Group",
            yaxis_title="Exam Score",
        )
        st.plotly_chart(fig_study, use_container_width=True)


def learning_style_tab(df: pd.DataFrame):
    st.markdown("### 🧠 Learning Styles – Do They Really Matter?")
    st.markdown(
        "<p class='section-subtitle'>See how different learning preferences relate to performance and behavior.</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>Average Exam Score by Learning Style</div>", unsafe_allow_html=True)
        group_ls = df.groupby("LearningStyle")["ExamScore"].mean().reset_index()
        fig_ls_score = px.bar(
            group_ls,
            x="LearningStyle",
            y="ExamScore",
            title="Average Exam Score by Learning Style",
            text="ExamScore",
        )
        fig_ls_score.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_ls_score.update_layout(
            template="plotly_dark",
            xaxis_title="Learning Style",
            yaxis_title="Average Exam Score",
        )
        st.plotly_chart(fig_ls_score, use_container_width=True)

    with col2:
        if "PerformanceCategory" in df.columns:
            st.markdown("<div class='section-title'>Performance Mix within Each Learning Style</div>", unsafe_allow_html=True)
            perf_by_ls = (
                df.groupby(["LearningStyle", "PerformanceCategory"])
                .size()
                .reset_index(name="Count")
            )
            fig_ls_perf = px.bar(
                perf_by_ls,
                x="LearningStyle",
                y="Count",
                color="PerformanceCategory",
                title="Performance Categories by Learning Style",
                barmode="stack",
            )
            fig_ls_perf.update_layout(
                template="plotly_dark",
                xaxis_title="Learning Style",
                yaxis_title="Number of Students",
            )
            st.plotly_chart(fig_ls_perf, use_container_width=True)

    # Engagement vs Learning style (e.g., StudyHours or Discussions)
    st.markdown("<div class='section-title'>Engagement Patterns by Learning Style</div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-subtitle'>Which learning styles tend to study more or participate more?</p>",
        unsafe_allow_html=True,
    )

    metrics = []
    if "StudyHours" in df.columns:
        metrics.append("StudyHours")
    if "Discussions" in df.columns:
        metrics.append("Discussions")
    if "AssignmentCompletion" in df.columns:
        metrics.append("AssignmentCompletion")

    if metrics:
        metric_choice = st.selectbox(
            "Choose engagement metric",
            metrics,
            index=0,
            help="Compare different engagement metrics across learning styles",
        )
        group_eng = df.groupby("LearningStyle")[metric_choice].mean().reset_index()
        fig_eng = px.bar(
            group_eng,
            x="LearningStyle",
            y=metric_choice,
            title=f"Average {metric_choice} by Learning Style",
            text=metric_choice,
        )
        fig_eng.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        fig_eng.update_layout(
            template="plotly_dark",
            xaxis_title="Learning Style",
            yaxis_title=f"Average {metric_choice}",
        )
        st.plotly_chart(fig_eng, use_container_width=True)


def stress_motivation_tab(df: pd.DataFrame):
    st.markdown("### ⚠ Stress & Motivation – The Hidden Factors")
    st.markdown(
        "<p class='section-subtitle'>Explore how stress and motivation are linked to performance.</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-title'>Stress vs Exam Score</div>", unsafe_allow_html=True)
        fig_stress = px.scatter(
            df,
            x="StressLevel",
            y="ExamScore",
            color="PerformanceCategory" if "PerformanceCategory" in df.columns else None,
            title="Stress Level vs Exam Score",
        )
        fig_stress.update_layout(
            template="plotly_dark",
            xaxis_title="Stress Level",
            yaxis_title="Exam Score",
        )
        st.plotly_chart(fig_stress, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>Motivation vs Exam Score</div>", unsafe_allow_html=True)
        fig_mot = px.scatter(
            df,
            x="Motivation",
            y="ExamScore",
            color="PerformanceCategory" if "PerformanceCategory" in df.columns else None,
            title="Motivation vs Exam Score",
        )
        fig_mot.update_layout(
            template="plotly_dark",
            xaxis_title="Motivation Level",
            yaxis_title="Exam Score",
        )
        st.plotly_chart(fig_mot, use_container_width=True)

    st.markdown("<div class='section-title'>Average Stress & Motivation (Current View)</div>", unsafe_allow_html=True)
    avg_stress = df["StressLevel"].mean()
    avg_mot = df["Motivation"].mean()
    col_a, col_b = st.columns(2)
    with col_a:
        metric_card("Avg Stress Level", f"{avg_stress:.1f}")
    with col_b:
        metric_card("Avg Motivation", f"{avg_mot:.1f}")

    st.markdown("<div class='section-title'>Interpretation & Suggestions</div>", unsafe_allow_html=True)

    insights = []
    if avg_stress >= 8:
        insights.append("Stress levels are **high on average**. Consider providing counselling, stress-management workshops and flexible deadlines.")
    elif avg_stress >= 5:
        insights.append("Stress levels are **moderate**. Monitor during exam periods and offer support proactively.")
    else:
        insights.append("Average stress is **relatively low**, but individual students may still need support.")

    if avg_mot <= 4:
        insights.append("Motivation appears **low**. Introduce goal-setting sessions, peer mentoring and more feedback on progress.")
    elif avg_mot <= 7:
        insights.append("Motivation is **moderate**. Small nudges like recognition, progress tracking and rewards can help.")
    else:
        insights.append("Motivation is **high on average**. Focus on maintaining engagement and providing challenging tasks.")

    for text in insights:
        st.markdown(f"- {text}")


def main():
    st.set_page_config(
        page_title="Student Performance Analytics Dashboard",
        layout="wide",
    )
    add_light_minimal_theme()
    df = load_data()

    # Sidebar filters – readable options
    st.sidebar.title("🎓 Filters")

    gender_options = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    gender = st.sidebar.selectbox("Gender", gender_options)

    learning_options = ["All"] + sorted(df["LearningStyle"].dropna().unique().tolist())
    learning_style = st.sidebar.selectbox("Learning Style", learning_options)

    # Attendance filter
    min_att, max_att = float(df["Attendance"].min()), float(df["Attendance"].max())
    att_range = st.sidebar.slider(
        "Attendance (%)",
        min_att,
        max_att,
        (min_att, max_att),
    )

    # Filter dataframe
    filtered_df = df.copy()
    if gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == gender]
    if learning_style != "All":
        filtered_df = filtered_df[filtered_df["LearningStyle"] == learning_style]
    filtered_df = filtered_df[
        (filtered_df["Attendance"] >= att_range[0]) &
        (filtered_df["Attendance"] <= att_range[1])
    ]

        # Hero / banner
    st.markdown(
        """
        <div class="hero-container">
            <div>
                <div class="hero-pill">
                    🎓 Student Analytics • End-to-End
                </div>
                <div class="hero-left-title">
                    Student Performance Analytics Dashboard
                </div>
                <div class="hero-left-subtitle">
                    Analyze study habits, attendance, learning styles, stress and motivation
                    to understand how they influence exam performance and final grades.
                </div>
                <div class="hero-tags">
                    <span class="hero-tag">Study Hours</span>
                    <span class="hero-tag">Attendance</span>
                    <span class="hero-tag">Learning Styles</span>
                    <span class="hero-tag">Stress</span>
                    <span class="hero-tag">Motivation</span>
                </div>
            </div>
            <div class="hero-right-card">
                <div class="hero-right-header">
                    <div class="hero-right-title">Current Cohort Snapshot</div>
                    <div class="hero-right-badge">Live view</div>
                </div>
                <div class="hero-right-bars">
                    <div class="hero-right-bar-row">
                        <div class="hero-right-bar-label">Exam Score</div>
                        <div class="hero-right-bar-track">
                            <div class="hero-right-bar-fill" style="width: 72%;"></div>
                        </div>
                    </div>
                    <div class="hero-right-bar-row">
                        <div class="hero-right-bar-label">Attendance</div>
                        <div class="hero-right-bar-track">
                            <div class="hero-right-bar-fill" style="width: 84%;"></div>
                        </div>
                    </div>
                    <div class="hero-right-bar-row">
                        <div class="hero-right-bar-label">Motivation</div>
                        <div class="hero-right-bar-track">
                            <div class="hero-right-bar-fill" style="width: 65%;"></div>
                        </div>
                    </div>
                </div>
                <div class="hero-metrics-row">
                    <div class="hero-metric-chip">
                        <div class="hero-metric-label">Students</div>
                        <div class="hero-metric-value">14,003</div>
                    </div>
                    <div class="hero-metric-chip">
                        <div class="hero-metric-label">High performers</div>
                        <div class="hero-metric-value">↑ data‑driven</div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # Tabs for sections
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📊 Overview",
            "🎯 Attendance & Study Habits",
            "🧠 Learning Styles",
            "⚠ Stress & Motivation",
        ]
    )

    with tab1:
        overview_tab(filtered_df)
    with tab2:
        attendance_study_tab(filtered_df)
    with tab3:
        learning_style_tab(filtered_df)
    with tab4:
        stress_motivation_tab(filtered_df)

    st.markdown("---")
    st.caption("Built by B M Bharath • Student Performance Analytics Dashboard")


if __name__ == "__main__":
    main()
