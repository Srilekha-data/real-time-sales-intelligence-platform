from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Real-Time Sales Dashboard", layout="wide")

st.title("🚀 Real-Time Sales Intelligence Dashboard")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "live_sales.csv"

@st.cache_data(ttl=3)
def load_data():
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame(columns=["order_id", "order_date", "product", "region", "sales", "quantity"])

df = load_data()

st.subheader("📊 Live Sales Data")
st.dataframe(df.tail(20), use_container_width=True)

if not df.empty:
    total_sales = int(df["sales"].sum())
    total_orders = int(df.shape[0])
    avg_order_value = round(df["sales"].mean(), 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"${total_sales}")
    col2.metric("📦 Total Orders", total_orders)
    col3.metric("📈 Avg Order Value", f"${avg_order_value}")

    st.subheader("📈 Sales by Product")
    product_sales = df.groupby("product")["sales"].sum().sort_values(ascending=False)
    st.bar_chart(product_sales)

    st.subheader("🌍 Sales by Region")
    region_sales = df.groupby("region")["sales"].sum().sort_values(ascending=False)
    st.bar_chart(region_sales)

    st.subheader("🚨 Anomaly Detection")
    threshold = df["sales"].mean() + 2 * df["sales"].std()
    anomalies = df[df["sales"] > threshold]

    if not anomalies.empty:
        st.error(f"⚠️ High sales spike detected! {len(anomalies)} unusual transactions")
        st.dataframe(anomalies.tail(5), use_container_width=True)
    else:
        st.success("✅ No anomalies detected")

    st.subheader("🤖 AI Business Insights")
    top_region = region_sales.idxmax()
    top_product = product_sales.idxmax()
    worst_product = product_sales.idxmin()

    recent_avg = df["sales"].tail(min(20, len(df))).mean()
    earlier_avg = df["sales"].head(min(20, len(df))).mean()
    growth = recent_avg - earlier_avg

    insight = f"""
📊 Business Summary:

• 🔝 Top Region: {top_region}
• 🏆 Best Product: {top_product}
• 📉 Underperforming Product: {worst_product}
• 📈 Sales Trend: {"Increasing 📈" if growth > 0 else "Decreasing 📉"}

💡 Recommendation:
Focus marketing on {top_product} in {top_region}.
Improve performance of {worst_product}.
"""

    st.info(insight)
    st.caption("Refresh the page to see the newest streamed records.")
else:
    st.warning("No live sales data yet. Keep the data generator running.")
    st.caption("⚡ Real-time pipeline refreshing every few seconds")