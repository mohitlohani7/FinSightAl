import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def show_overview(df: pd.DataFrame):
    """Display basic dataset info."""
    st.subheader("Dataset Overview")
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")
    st.dataframe(df.head())

def transaction_trend(df: pd.DataFrame):
    """Show transaction trends over time."""
    if "Date" in df.columns:
        trend = df.groupby(df["Date"].dt.date)["Amount"].sum()
        fig, ax = plt.subplots()
        trend.plot(ax=ax)
        ax.set_title("Transaction Trend Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Amount")
        st.pyplot(fig)
    else:
        st.warning("No 'Date' column found for trend analysis.")

def spending_by_merchant(df: pd.DataFrame):
    """Show spending by merchant."""
    if "Merchant" in df.columns:
        merchant_spending = df.groupby("Merchant")["Amount"].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots()
        merchant_spending.plot(kind="bar", ax=ax)
        ax.set_title("Top 10 Merchants by Spending")
        ax.set_xlabel("Merchant")
        ax.set_ylabel("Total Amount")
        st.pyplot(fig)
    else:
        st.warning("No 'Merchant' column found for spending analysis.")

def interactive_plotly_amounts(df: pd.DataFrame):
    """Interactive plot of amounts over time using Plotly."""
    if "Date" in df.columns and "Amount" in df.columns:
        fig = px.scatter(df, x="Date", y="Amount", color="Merchant", title="Transaction Amounts Over Time")
        st.plotly_chart(fig)
    else:
        st.warning("Required columns ('Date', 'Amount') missing for interactive plot.")
