import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Nassau Candy Profitability Analysis", layout="wide"
)

st.title("🍬 Nassau Candy Distributor - Profitability & Margin Analysis")

# Load Data
df = pd.read_csv('Nassau Candy Distributor.csv')
df["Gross Margin (%)"] = (df["Gross Profit"] / df["Sales"]) * 100

# Sidebar Filters
st.sidebar.header("Filter Options")
division = st.sidebar.multiselect(
    "Select Division:",
    options=df["Division"].unique(),
    default=df["Division"].unique(),
)

df_filtered = df[df["Division"].isin(division)]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${df_filtered['Gross Profit'].sum():,.2f}")
col3.metric(
    "Avg Margin",
    f"{(df_filtered['Gross Profit'].sum() / df_filtered['Sales'].sum()) * 100:.2f}%",
)

st.subheader("Division Performance")
fig = px.bar(
    df_filtered,
    x="Division",
    y="Gross Profit",
    color="Division",
    title="Gross Profit by Division",
)
st.plotly_chart(fig, use_container_width=True)


import plotly.express as px
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Nassau Candy Profitability Analysis", layout="wide")

st.title("🍬 Nassau Candy Distributor - Product Line Profitability & Margin Analysis")

# Load Data
df = pd.read_csv("Nassau Candy Distributor.csv")
df["Gross Margin (%)"] = (df["Gross Profit"] / df["Sales"]) * 100
df["Profit per Unit"] = df["Gross Profit"] / df["Units"]

# Sidebar Filters
st.sidebar.header("Filter Dashboard")
selected_division = st.sidebar.multiselect(
    "Select Division:",
      options=df["Division"].unique(),
        default=df["Division"].unique(),
        key="unique_division_select"
)
min_margin = st.sidebar.slider("Minimum Gross Margin (%)", 0.0, 100.0, 0.0)

# Filter Data
filtered_df = df[(df["Division"].isin(selected_division)) & (df["Gross Margin (%)"] >= min_margin)]

# Top Key Performance Indicators (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_df['Gross Profit'].sum():,.2f}")
col3.metric("Total Units Sold", f"{filtered_df['Units'].sum():,}")
avg_margin_val = (filtered_df['Gross Profit'].sum() / filtered_df['Sales'].sum()) * 100 if filtered_df['Sales'].sum() > 0 else 0
col4.metric("Average Gross Margin", f"{avg_margin_val:.2f}%")

st.markdown("---")

# Dashboard Tabs
tab1, tab2, tab3 = st.tabs(["📊 Product Profitability", "🏬 Division Analysis", "⚠️ Risk & Cost Diagnostics"])

with tab1:
    st.subheader("Top Products Leaderboard")
    prod_df = filtered_df.groupby("Product Name").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Avg_Margin=("Gross Margin (%)", "mean")
    ).reset_index().sort_values(by="Total_Profit", ascending=False)
    
    col_a, col_b = st.columns(2)
    with col_a:
        fig_prod = px.bar(prod_df.head(10), x="Total_Profit", y="Product Name", orientation="h",
                          title="Top 10 Products by Gross Profit", color="Total_Profit", color_continuous_scale="Viridis")
        st.plotly_chart(fig_prod, use_container_width=True)
    with col_b:
        fig_scatter = px.scatter(filtered_df, x="Sales", y="Gross Profit", color="Division",
                                 size="Units", hover_data=["Product Name"], title="Sales vs Gross Profit Scatter Plot")
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.subheader("Division Performance Breakdown")
    div_df = filtered_df.groupby("Division").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    ).reset_index()
    
    fig_div = px.bar(div_df, x="Division", y=["Total_Sales", "Total_Profit"], barmode="group",
                     title="Revenue vs Profit Imbalance by Division")
    st.plotly_chart(fig_div, use_container_width=True)

with tab3:
    st.subheader("Low Margin Risk Products")
    low_margin_df = filtered_df[filtered_df["Gross Margin (%)"] < 50]
    st.dataframe(low_margin_df[["Order ID", "Product Name", "Division", "Sales", "Cost", "Gross Profit", "Gross Margin (%)"]])