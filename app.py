import streamlit as st
from config import settings
from modules.data_loader import load_csv, basic_clean
from modules.anomaly_detection import detect_anomalies
import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    # Make sure 'Amount' column exists
    if 'Amount' not in df.columns:
        raise KeyError("Column 'Amount' is missing from the dataset!")

    # Use only numeric columns for anomaly detection
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        raise ValueError("No numeric columns found for anomaly detection.")

    data = df[numeric_cols].dropna()

    # Initialize Isolation Forest model
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(data)

    # Predict anomalies (-1 = anomaly, 1 = normal)
    preds = model.predict(data)

    # Create a copy of df and add a boolean column 'is_anomaly'
    df_anom = df.loc[data.index].copy()
    df_anom['is_anomaly'] = preds == -1

    return df_anom

from modules.eda_analysis import (
    show_overview,
    transaction_trend,
    spending_by_merchant,
    interactive_plotly_amounts
)
from modules.anomaly_detection import detect_anomalies
from modules.ai_agent import generate_insights_from_df, generate_insights_from_df_with_question
from modules.report_generator import make_simple_pdf_report

# Streamlit page settings
st.set_page_config(page_title=settings.APP_TITLE, layout="wide")
st.title(settings.APP_TITLE)
st.caption(settings.APP_DESCRIPTION)

uploaded = st.file_uploader("Upload transaction CSV (any platform)", type=["csv"])

if uploaded is not None:
    try:
        df = load_csv(uploaded)
        df = basic_clean(df)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    st.sidebar.header("Analysis Tools")
    show_preview = st.sidebar.checkbox("Show dataset preview", value=True)
    run_eda = st.sidebar.checkbox("Run EDA", value=True)
    run_anom = st.sidebar.checkbox("Run anomaly detection", value=True)
    run_ai = st.sidebar.checkbox("Generate AI insights (Groq)", value=True)

    if show_preview:
        show_overview(df)

    if run_eda:
        st.markdown("---")
        st.header("Exploratory Data Analysis")
        transaction_trend(df)
        spending_by_merchant(df)
        interactive_plotly_amounts(df)

    if run_anom:
        st.markdown("---")
        st.header("Anomaly Detection")
        result = detect_anomalies(df)
        st.write("Top flagged anomalies:")
        st.dataframe(result[result.is_anomaly].head(25))

    if run_ai:
        st.markdown("---")
        st.header("AI Insights")

        # Step 1: Automatic AI summary
        with st.spinner("Generating insights from Groq..."):
            auto_summary = generate_insights_from_df(df)
        st.text_area("AI Auto Summary", auto_summary, height=250)

        # Step 2: Interactive chat
        st.markdown("### Ask FinSight AI")
        user_input = st.text_input("Type your question here:")

        if st.button("Ask AI"):
            if user_input.strip() != "":
                with st.spinner("Getting answer from Groq..."):
                    answer = generate_insights_from_df_with_question(df, user_input)
                    st.text_area("AI Answer", answer, height=200)
            else:
                st.warning("Please enter a question!")

    st.markdown("---")
    if st.button("Download PDF report of AI insights"):
        with st.spinner("Generating PDF..."):
            ai_text = generate_insights_from_df(df) or "No insights available"
            pdf_bytes = make_simple_pdf_report("FinSight AI Report", ai_text)
            st.download_button(
                "Download Report",
                data=pdf_bytes,
                file_name="finsight_report.pdf",
                mime="application/pdf"
            )

else:
    st.info("Upload a CSV file to get started. A sample CSV is included in /data.")
