import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="APP Pulse AI",
    layout="wide",
    page_icon="🚀"
)

# =========================
# CUSTOM UI STYLE
# =========================

st.markdown("""
<style>

.main {
    background-color: #f6f8fc;
}

h1, h2, h3 {
    color: #0f172a;
    font-weight: 700;
}

section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] * {
    color: #111827 !important;
    font-weight: 500;
}

div[data-testid="stDataFrame"] {
    background-color: #ffffff;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 15px;
    border-radius: 12px;
}

button {
    background-color: #2563eb !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

.js-plotly-plot {
    background-color: white !important;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR NAVIGATION
# =========================

st.sidebar.title("🚀 APP Pulse AI")

page = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "📈 Metrics", "🚨 Alerts"]
)

# =========================
# SESSION STATE
# =========================

if "df" not in st.session_state:
    st.session_state.df = None

# =========================
# LOAD DATA FUNCTION
# =========================

@st.cache_data
def load_data(file):
    df = pd.read_excel(file, engine="odf")
    df.columns = [col.strip() for col in df.columns]
    return df


# =========================
# GET DATA FROM SESSION
# =========================

df = st.session_state.df

# =========================
# DASHBOARD PAGE
# =========================

if page == "📊 Dashboard":

    st.title("🚀 APP Pulse AI")
    st.subheader("Application Performance Monitoring & Regression Detector")


    uploaded_file = st.file_uploader(
        "📁 Upload ODS File",
        type=["ods"]
    )

    if uploaded_file:

        df = load_data(uploaded_file)
        st.session_state.df = df

        st.success("✅ File loaded successfully!")

    # =========================
    # SHOW DATA AFTER UPLOAD
    # =========================

    df = st.session_state.df

    if df is not None:

        st.markdown("## 📊 Data Preview")
        st.dataframe(df, use_container_width=True)

    else:
        st.info("Upload a file to start analysis.")
# =========================
# METRICS PAGE
# =========================

elif page == "📈 Metrics":

    st.markdown("## 📈 Metrics Over Time")

    if df is None:
        st.warning("Please upload data from Dashboard first.")
    else:

        if "Time" in df.columns:
            df["Time"] = df["Time"].astype(str)

            metrics = [c for c in df.columns if c not in ["Time", "Event"]]

            for i in range(0, len(metrics), 2):

                col1, col2 = st.columns(2)

                with col1:
                    m = metrics[i]

                    fig = px.line(df, x="Time", y=m, title=f"{m} Trend")

                    fig.update_layout(
                        height=280,
                        margin=dict(l=20, r=20, t=40, b=20),
                        plot_bgcolor="white",
                        paper_bgcolor="white"
                    )

                    st.plotly_chart(fig, use_container_width=True)

                if i + 1 < len(metrics):
                    with col2:
                        m = metrics[i + 1]

                        fig = px.line(df, x="Time", y=m, title=f"{m} Trend")

                        fig.update_layout(
                            height=280,
                            margin=dict(l=20, r=20, t=40, b=20),
                            plot_bgcolor="white",
                            paper_bgcolor="white"
                        )

                        st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("Time column not found in dataset.")

# =========================
# ALERTS PAGE (LLM READY)
# =========================

elif page == "🚨 Alerts":

    st.title("🚨 Simple Regression Alert Checker")

    # =========================
    # GET DATA FROM SESSION
    # =========================
    df = st.session_state.get("df", None)

    if df is None:
        st.warning("⚠️ No data found. Please upload file from Dashboard first.")
        st.stop()

    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    # =========================
    # VALIDATION
    # =========================
    if "Time" not in df.columns:
        st.error("❌ 'Time' column missing in dataset")
        st.stop()

    df["Time"] = df["Time"].astype(str)
    time_options = df["Time"].tolist()

    # =========================
    # SIDEBAR TIME FILTER
    # =========================
    st.sidebar.header("📅 Select Time Range")

    start_time = st.sidebar.selectbox("Start Time", time_options, index=0)
    end_time = st.sidebar.selectbox("End Time", time_options, index=len(time_options)-1)

    start_idx = time_options.index(start_time)
    end_idx = time_options.index(end_time)

    filtered_df = df.iloc[start_idx:end_idx+1].copy()

    # =========================
    # HEADER
    # =========================
    st.subheader(f"Analyzing Data From **{start_time} → {end_time}**")
    st.write(f"Total records analyzed: **{len(filtered_df)}**")

    st.divider()

    # =========================
    # THRESHOLD ENGINE
    # =========================
    def calculate_thresholds(df):
        
        thresholds = {}

        for col in df.columns:
            if col == "Time":
                continue

            if not pd.api.types.is_numeric_dtype(df[col]):
                continue

            mean = df[col].mean()
            std = df[col].std() if df[col].std() > 0 else 1

            # Cache Hit rule (lower is bad)
            if "cache" in col.lower():
                thresholds[col] = mean - 2 * std
            else:
                thresholds[col] = mean + 2 * std

        return thresholds

    thresholds = calculate_thresholds(df)
    

    # =========================
    # ALERT CHECK FUNCTION
    # =========================
    def check_row_alerts(row):
        alerts = []

        for metric, threshold in thresholds.items():

            if metric not in row or pd.isna(row[metric]):
                continue

            value = row[metric]

            if "cache" in metric.lower():
                if value < threshold:
                    alerts.append(f"{metric} = {value} (< {round(threshold,2)})")
            else:
                if value > threshold:
                    alerts.append(f"{metric} = {value} (> {round(threshold,2)})")

        return alerts

    # =========================
    # OUTPUT
    # =========================
    st.subheader("🚨 Per Timestamp Alerts")

    alert_found = False

    for _, row in filtered_df.iterrows():

        row_alerts = check_row_alerts(row)

        with st.expander(f"📍 {row['Time']}", expanded=False):

            st.write("### Metrics")

            for col in df.columns:
                if col == "Time":
                    continue
                if col in row:
                    st.write(f"- **{col}**: {row[col]}")

            st.write("")

            if row_alerts:
                alert_found = True
                st.error("🚨 Alerts Triggered")
                for a in row_alerts:
                    st.warning(f"⚠️ {a}")
            else:
                st.success("✅ No alerts")

    st.divider()

    # =========================
    # SUMMARY
    # =========================
    if alert_found:
        st.warning("⚠️ Regression anomalies detected in selected time range.")
    else:
        st.success("🎉 No regression alerts found!")

    # =========================
    # TABLE VIEW
    # =========================
    st.subheader("Filtered Data Table")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

    # =========================
    # SIDEBAR THRESHOLDS
    # =========================
    st.sidebar.divider()
    st.sidebar.subheader("Thresholds Used")

    for k, v in thresholds.items():
        if "cache" in k.lower():
            st.sidebar.write(f"**{k}** < {round(v,2)}")
        else:
            st.sidebar.write(f"**{k}** > {round(v,2)}")