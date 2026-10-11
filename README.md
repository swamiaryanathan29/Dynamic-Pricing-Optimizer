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

**PriceOptima** models empirical **Price Elasticity of Demand** ($\epsilon$) to find the mathematical "sweet spot" discount tier that meets liquidation hurdles while preserving gross margins.

---

## ⚙️ Key Technical & Trading Formulations

### 1. Price Elasticity of Demand Estimation
Estimates empirical category and SKU elasticity using a log-log regression formulation:
$$\ln(Q) = \alpha + \epsilon \cdot \ln(P)$$
Where:
* $Q$ = Expected weekly unit volume
* $P$ = Net effective price post-discount
* $\epsilon$ = Price elasticity coefficient ($\epsilon < -1$ indicates price-elastic demand)

### 2. Markdown Optimization Formulation
Finds the optimal discount tier $d^* \in \{0\%, 10\%, 15\%, 20\%, 30\%, 40\%, 50\%\}$ to:
$$\max_{d} \quad \text{Gross Profit} = \sum_{w=1}^{W} \Big( P \cdot (1 - d) - \text{COGS} \Big) \times Q(P, d)$$
Subject to:
$$\text{Gross Margin } \% \ge \text{Target Margin Hurdle (e.g., 38\%) }$$
$$\text{Sell-Through Rate (STR) } \% \ge \text{Target Liquidation Hurdle (e.g., 75\%) }$$

### 3. Interactive Web Sandbox & Excel Reporting
* **Revenue vs. Margin Trade-off Visualizer:** Side-by-side comparison of projected top-line revenue vs bottom-line margin across promotional discount tiers.
* **Operational Excel Export:** Generates an enterprise-ready merchandising plan `.xlsx` for store ops and digital trading leads.

---

## 📁 Repository Structure
```text
├── app.py                      # Interactive Streamlit trading application
├── pricing_engine.py           # Elasticity log-log regression & markdown optimizer
├── generate_trading_data.py    # Synthesizer for retail pricing, COGS & sell-through
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation and business context
```

---

## 🚀 Quickstart Guide

### 1. Clone the repository
```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/retail-markdown-pricing-optimizer.git
cd retail-markdown-pricing-optimizer
```

### 2. Set up virtual environment & install dependencies
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 💼 Resume Description (For Trading & Revenue Management Roles)

**PriceOptima: Retail Markdown & Promotional Pricing Strategy Engine** | *Python, Scipy, Streamlit, Pandas*
* Developed an algorithmic pricing optimizer for End-of-Season Sales (EOSS) across 15+ footwear and apparel SKUs.
* Modeled empirical price elasticity ($\epsilon$) using log-log regression to simulate consumer discount sensitivity.
* Formulated a constrained optimization solver balancing gross margin hurdle rates and inventory liquidation targets, generating commercial trading schedules exportable to Excel.
