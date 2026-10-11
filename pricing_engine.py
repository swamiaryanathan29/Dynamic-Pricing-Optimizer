import pandas as pd
import numpy as np
import os

def load_trading_data(filepath="data/trading_markdown_data.csv"):
    if not os.path.exists(filepath):
        from generate_trading_data import generate_trading_data
        generate_trading_data(filepath)
    df = pd.read_csv(filepath)
    return df

def fit_elasticity_model(df, sku_name):
    """Calculates empirical price elasticity using log-log regression: ln(Q) = alpha + beta * ln(P)"""
    sku_data = df[df["sku_name"] == sku_name].copy()
    if len(sku_data) < 3:
        return -2.0, sku_data
        
    log_p = np.log(sku_data["effective_price"])
    log_q = np.log(sku_data["weekly_units_sold"])
    
    slope, intercept = np.polyfit(log_p, log_q, 1)
    return round(slope, 2), sku_data

def optimize_markdown_strategy(df, sku_name, weeks_remaining=4, min_margin_hurdle=35.0, target_sell_through=75.0):
    """
    Finds the optimal discount tier that balances:
    - Target sell-through rate (clearing seasonal inventory)
    - Protecting gross margin hurdle rate (%)
    - Maximizing total gross profit INR
    """
    sku_rows = df[df["sku_name"] == sku_name].copy()
    if sku_rows.empty:
        return None
        
    candidates = []
    
    for _, row in sku_rows.iterrows():
        discount = row["discount_pct"]
        weekly_units = row["weekly_units_sold"]
        total_units_cycle = min(weekly_units * weeks_remaining, row["initial_stock"])
        str_pct = round((total_units_cycle / row["initial_stock"]) * 100, 2)
        
        cycle_revenue = round(total_units_cycle * row["effective_price"], 2)
        cycle_cogs = round(total_units_cycle * row["cogs"], 2)
        cycle_gross_profit = round(cycle_revenue - cycle_cogs, 2)
        margin_pct = round((cycle_gross_profit / cycle_revenue) * 100, 2) if cycle_revenue > 0 else 0
        
        is_feasible = (margin_pct >= min_margin_hurdle) and (str_pct >= target_sell_through)
        
        candidates.append({
            "discount_pct": discount,
            "effective_price": row["effective_price"],
            "weekly_demand": weekly_units,
            "projected_units_sold": total_units_cycle,
            "sell_through_rate_pct": str_pct,
            "cycle_revenue_inr": cycle_revenue,
            "gross_profit_inr": cycle_gross_profit,
            "gross_margin_pct": margin_pct,
            "is_feasible": is_feasible
        })
        
    result_df = pd.DataFrame(candidates)
    
    feasible_df = result_df[result_df["is_feasible"] == True]
    if not feasible_df.empty:
        best_choice = feasible_df.sort_values("gross_profit_inr", ascending=False).iloc[0]
        recommendation_status = "Optimal Feasible Plan"
    else:
        margin_ok_df = result_df[result_df["gross_margin_pct"] >= min_margin_hurdle]
        if not margin_ok_df.empty:
            best_choice = margin_ok_df.sort_values("gross_profit_inr", ascending=False).iloc[0]
            recommendation_status = "Margin Hurdle Honored (Sell-Through Shortfall)"
        else:
            best_choice = result_df.sort_values("gross_profit_inr", ascending=False).iloc[0]
            recommendation_status = "Profit Maximizing (Below Hurdle)"
            
    return {
        "best_tier": best_choice.to_dict(),
        "all_tiers": result_df,
        "recommendation_status": recommendation_status
    }
