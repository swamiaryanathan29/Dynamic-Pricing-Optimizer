# 🏷️ PriceOptima: Retail Markdown & Promotional Pricing Optimizer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An algorithmic commercial decision-support engine built for **Trading & Revenue Management** in modern retail. Maximizes gross profit and inventory liquidation during promotional events and End-of-Season Sales (EOSS).

---

## 🎯 Business Problem & Context
During promotional events (EOSS, Festive Promotions, Flash Sales), commercial trading teams face a classic profit paradox:
* **Discount too little:** Inventory fails to clear before the next seasonal drop arrives, accumulating dead stock and holding costs in warehouses.
* **Discount too deeply:** Retailers trigger margin erosion, where high transaction volume fails to generate target gross profitability.

**PriceOptima** models empirical **Price Elasticity of Demand** to find the mathematical "sweet spot" discount tier that meets liquidation hurdles while preserving gross margins.

---

## ⚙️ Key Technical & Trading Formulations

### 1. Price Elasticity of Demand Estimation
Estimates empirical category and SKU elasticity using a log-log regression formulation:

```text
ln(Q) = α + ε · ln(P)
```

* **Q** = Expected weekly unit volume
* **P** = Net effective price post-discount
* **ε** = Price elasticity coefficient (`ε < -1` indicates price-elastic demand)

### 2. Markdown Optimization Formulation
Evaluates candidate discount tiers `d ∈ {0%, 10%, 15%, 20%, 30%, 40%, 50%}` to maximize total campaign profitability:

```text
Maximize:
  Gross Profit = Σ [ P · (1 - d) - COGS ] × Q(P, d)

Subject to:
  Gross Margin %  ≥  Target Margin Hurdle Rate (e.g., 38%)
  Sell-Through %  ≥  Target Liquidation Goal (e.g., 75%)
```

### 3. Interactive Web Sandbox & Excel Reporting
* **Revenue vs. Margin Trade-off Visualizer:** Side-by-side comparison of projected top-line revenue vs bottom-line margin across promotional discount tiers.
* **Operational Excel Export:** Generates an enterprise-ready merchandising plan `.xlsx` for store ops and digital trading leads.

---

## 🖥️ Live Local Interface
When running locally, your browser will automatically open with **PriceOptima** at:
👉 `http://localhost:8502`

**Interactive Capabilities in the UI:**
* 📈 View empirical price elasticity curves across footwear and apparel categories.
* ⚖️ Side-by-side Revenue vs. Gross Profit margin trade-off visualizer.
* 🎯 Commercial markdown optimization grid with constraint feasibility flags.
* 📥 One-click export of the commercial trading strategy into an operational Excel spreadsheet (`.xlsx`).

---

## 📁 Repository Modules & File Links

* 🖥️ **[`app.py`](./app.py)** — Interactive Streamlit commercial trading dashboard.
* ⚙️ **[`pricing_engine.py`](./pricing_engine.py)** — Empirical price elasticity estimation and constrained markdown optimization solver.
* 📊 **[`generate_trading_data.py`](./generate_trading_data.py)** — Retail pricing, COGS, and discount tier transaction generator.
* 📈 **[`data/trading_markdown_data.csv`](./data/trading_markdown_data.csv)** — Category-level pricing elasticity and sell-through dataset.
* 📦 **[`requirements.txt`](./requirements.txt)** — Core Python package dependencies.
