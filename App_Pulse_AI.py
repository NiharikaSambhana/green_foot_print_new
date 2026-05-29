import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="APP Pulse AI", layout="wide")

st.title("🚀 APP Pulse AI")
st.subheader("Application Performance Monitoring & Regression Detector")

# -----------------------------
# Upload ODS File
# -----------------------------
uploaded_file = st.file_uploader("Upload ODS File", type=["ods"])

@st.cache_data
def load_data(file):
    df = pd.read_excel(file, engine="odf")

    # Clean column names (fix merged headers like "CPU %Memory %")
    df.columns = [col.strip() for col in df.columns]

    return df


if uploaded_file:
    df = load_data(uploaded_file)

    st.success("File loaded successfully!")

    # =========================
    # 📊 DISPLAY DATAFRAME ONLY
    # =========================

    st.write("### 📊 Uploaded Data")

    st.dataframe(df, use_container_width=True)


    # ==========================================
    # 📈 TIME SERIES PLOTS (2 per row)
    # ==========================================

    st.write("### 📈 Metrics Over Time")

    # Ensure Time column exists
    if "Time" in df.columns:

        # Convert Time if needed (safe fallback)
        df["Time"] = df["Time"].astype(str)

        metrics = [
            col for col in df.columns
            if col not in ["Time", "Event"]
        ]

        # Plot 2 charts per row
        for i in range(0, len(metrics), 2):
            col1, col2 = st.columns(2)

            # First chart in row
            with col1:
                metric = metrics[i]
                fig = px.line(
                    df,
                    x="Time",
                    y=metric,
                    title=f"{metric} over Time"
                )
                st.plotly_chart(fig, use_container_width=True)

            # Second chart in row (if exists)
            if i + 1 < len(metrics):
                with col2:
                    metric = metrics[i + 1]
                    fig = px.line(
                        df,
                        x="Time",
                        y=metric,
                        title=f"{metric} over Time"
                    )
                    st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Time column not found in dataset.")