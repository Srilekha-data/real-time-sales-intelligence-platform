from pathlib import Path
from datetime import datetime
import random

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Real-Time Sales Dashboard", layout="wide")

st.title("🚀 Real-Time Sales Intelligence Dashboard")
st.caption("⚡ Real-time pipeline simulation with AI-style business insights")

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "live_sales.csv"

PRODUCTS = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard"]
REGIONS = ["North", "South", "East", "West"]


def generate_data():
    return {
        "order_id": random.randint(1000, 9999),
        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "product": random.choice(PRODUCTS),
        "region": random.choice(REGIONS),
        "sales": random.randint(500, 2500),
        "quantity": random.randint(1, 5),
    }


def ensure_data_file():
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_PATH.exists():
        df = pd.DataFrame(columns=["order_id", "order_date", "product", "region", "sales", "quantity"])
        df.to_csv(DATA_PATH, index=False)


def append_simulated_rows(n=5):
    rows = [generate_data() for _ in range(n)]
    pd.DataFrame(rows).to_csv(DATA_PATH, mode="a", header=False, index=False)


@st.cache_data(ttl=3)
def load_data():
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)
    return pd.DataFrame(columns=["order_id", "order_date", "product", "region", "sales", "quantity"])


ensure_data_file()

if st.button("Generate New Live Batch"):
    append_simulated_rows(5)
    st.cache_data.clear()
    st.rerun()

if st.button("Reset Data"):
    pd.DataFrame(columns=["order_id", "order_date", "product", "region", "sales", "quantity"]).to_csv(DATA_PATH, index=False)
    st.cache_data.clear()
    st.rerun()

df = load_data()

st.subheader("📊 Live Sales Data")
st.dataframe(df.tail(20), use_container_width=True)

if not df.empty:
    total_sales = int(df["sales"].sum())
    total_orders = int(df.shape[0])
    avg_order_value = round(df["sales"].mean(), 2)

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Sales", f"${total_sales:,}")
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

    st.subheader("🔮 Sales Prediction (Next Trend)")
    if len(df) > 10:
        df["rolling_avg"] = df["sales"].rolling(5).mean()
        latest_trend = df["rolling_avg"].iloc[-1]
        previous_trend = df["rolling_avg"].iloc[-5]

        if latest_trend > previous_trend:
            st.success("📈 Sales are expected to increase in next period")
        else:
            st.warning("📉 Sales might decrease — monitor closely")

        st.line_chart(df["rolling_avg"])
else:
    st.warning("No live sales data yet. Click 'Generate New Live Batch' to simulate data.")