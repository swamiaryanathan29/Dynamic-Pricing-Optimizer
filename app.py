import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

from pricing_engine import (
    load_trading_data,
    fit_elasticity_model,
    optimize_markdown_strategy
)

st.set_page_config(
    page_title="PriceOptima | Retail Markdown & Pricing Optimizer",
    page_icon="🏷️",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #059669;
    }
</style>
""", unsafe_allow_html=True)

# Title Bar
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    st.title("🏷️ PriceOptima: Commercial Pricing Engine")
    st.subheader("Retail Markdown & Promotional Pricing Optimization Engine")
with col_h2:
    st.markdown("### `PriceOptima`\n**Trading & Yield Edition**")

st.markdown("---")

# Data loading
@st.cache_data
def get_data():
    return load_trading_data()

df = get_data()

# Sidebar Configuration
st.sidebar.header("🎯 Trading Parameters")

categories = list(df["category"].unique())
selected_category = st.sidebar.selectbox("Merchandise Category", categories)

skus_in_cat = list(df[df["category"] == selected_category]["sku_name"].unique())
selected_sku = st.sidebar.selectbox("Select Target SKU", skus_in_cat)

st.sidebar.markdown("---")
st.sidebar.subheader("Liquidation & Margin Constraints")

weeks_left = st.sidebar.slider("Promo Window (Weeks Remaining)", min_value=1, max_value=8, value=4)
target_str = st.sidebar.slider("Target Sell-Through Rate (%)", min_value=50, max_value=95, value=75, step=5)
min_margin = st.sidebar.slider("Minimum Gross Margin Hurdle (%)", min_value=25, max_value=55, value=38, step=1)

# Fit Elasticity & Run Optimizer
elasticity, sku_df = fit_elasticity_model(df, selected_sku)
opt_result = optimize_markdown_strategy(
    df, selected_sku,
    weeks_remaining=weeks_left,
    min_margin_hurdle=min_margin,
    target_sell_through=target_str
)

best_tier = opt_result["best_tier"]
all_tiers = opt_result["all_tiers"]
mrp_val = sku_df["mrp"].iloc[0]
cogs_val = sku_df["cogs"].iloc[0]

# KPI Metrics Bar
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Base MRP", f"₹{mrp_val:,.0f}")
with k2:
    st.metric("Cost of Goods (COGS)", f"₹{cogs_val:,.0f}")
with k3:
    st.metric(
        "Price Elasticity (ε)",
        f"{elasticity}",
        help="Values below -1 indicate price-elastic demand; discounts drive significant unit uplift."
    )
with k4:
    rec_discount = int(best_tier['discount_pct'])
    st.metric("Recommended Discount", f"{rec_discount}% OFF", delta=opt_result['recommendation_status'])
with k5:
    st.metric("Projected Gross Profit", f"₹{best_tier['gross_profit_inr']:,.0f}")

st.markdown("---")

tab1, tab2 = st.tabs(["📈 Elasticity & Revenue-Margin Frontier", "📋 Markdown Scenario Grid & Excel Export"])

with tab1:
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("1. Demand Curve vs. Discount Tier")
        fig_demand = px.line(
            all_tiers,
            x="discount_pct",
            y="weekly_demand",
            markers=True,
            title=f"Price Elasticity Response Curve ({selected_sku})",
            labels={"discount_pct": "Discount Offered (%)", "weekly_demand": "Weekly Units Sold"},
            line_shape="spline"
        )
        fig_demand.update_traces(line_color="#059669", line_width=3)
        fig_demand.update_layout(template="plotly_white")
        st.plotly_chart(fig_demand, use_container_width=True)
        
    with col_g2:
        st.subheader("2. Revenue vs. Gross Profit Trade-off")
        fig_tradeoff = go.Figure()
        fig_tradeoff.add_trace(go.Bar(
            x=[f"{d}%" for d in all_tiers["discount_pct"]],
            y=all_tiers["cycle_revenue_inr"],
            name="Cycle Revenue (INR)",
            marker_color="#1f2937"
        ))
        fig_tradeoff.add_trace(go.Bar(
            x=[f"{d}%" for d in all_tiers["discount_pct"]],
            y=all_tiers["gross_profit_inr"],
            name="Gross Profit (INR)",
            marker_color="#059669"
        ))
        fig_tradeoff.update_layout(
            barmode="group",
            title=f"{weeks_left}-Week Campaign: Revenue vs Profit at Each Discount",
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_tradeoff, use_container_width=True)

with tab2:
    st.subheader("📋 Commercial Markdown Decision Matrix")
    st.write(f"Evaluating liquidation plans for **{selected_sku}** over a **{weeks_left}-week promotion window**:")
    
    display_df = all_tiers.copy()
    display_df["Recommended"] = display_df["discount_pct"].apply(
        lambda x: "⭐ RECOMMENDED" if x == best_tier["discount_pct"] else ("✅ Feasible" if display_df.loc[display_df["discount_pct"]==x, "is_feasible"].values[0] else "❌ Violates Constraints")
    )
    
    columns_show = [
        "discount_pct", "effective_price", "projected_units_sold",
        "sell_through_rate_pct", "cycle_revenue_inr", "gross_profit_inr",
        "gross_margin_pct", "Recommended"
    ]
    
    rename_cols = {
        "discount_pct": "Discount Tier (%)",
        "effective_price": "Promo Price (₹)",
        "projected_units_sold": "Projected Units",
        "sell_through_rate_pct": "Sell-Through Rate (%)",
        "cycle_revenue_inr": "Total Revenue (₹)",
        "gross_profit_inr": "Gross Margin (₹)",
        "gross_margin_pct": "Gross Margin (%)",
        "Recommended": "Status"
    }
    
    final_table = display_df[columns_show].rename(columns=rename_cols)
    
    def highlight_rec(row):
        if "⭐" in row["Status"]:
            return ['background-color: #dcfce7; font-weight: bold'] * len(row)
        elif "❌" in row["Status"]:
            return ['background-color: #fee2e2'] * len(row)
        return [''] * len(row)
        
    st.dataframe(final_table.style.apply(highlight_rec, axis=1), use_container_width=True)
    
    # Export
    col_d1, col_d2 = st.columns([2, 1])
    with col_d1:
        st.caption("Commercial Trading Rule: Protects margin hurdle while clearing terminal stock before arrival of next season collection.")
    with col_d2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            final_table.to_excel(writer, index=False, sheet_name='Trading_Markdown_Plan')
        st.download_button(
            label="📥 Export Trading Strategy to Excel (.xlsx)",
            data=buffer.getvalue(),
            file_name=f"Trading_Markdown_Plan_{selected_sku.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.markdown("---")
st.caption("PriceOptima | Built with Python, NumPy & Streamlit")
