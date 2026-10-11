import csv
import random
import os

def generate_trading_data(output_path="data/trading_markdown_data.csv"):
    random.seed(101)
    
    categories = [
        {"category": "Performance Running", "skus": ["AeroPulse Nitro 3", "Carbon Elite Racer", "Veloce Stride Pro"], "mrp_range": (8999, 14999), "cogs_ratio": 0.38, "elasticity_base": -1.8},
        {"category": "Lifestyle & Streetwear", "skus": ["Heritage Court Suede", "Palermo Retro Classic", "Urban Low Leather"], "mrp_range": (4999, 8999), "cogs_ratio": 0.35, "elasticity_base": -2.3},
        {"category": "Motorsport Inspired", "skus": ["Scuderia Speed Cat", "Grand Prix Track Top", "Apex Racing Jersey"], "mrp_range": (3999, 10999), "cogs_ratio": 0.40, "elasticity_base": -1.4},
        {"category": "Training & Activewear", "skus": ["AeroDry Tech Hoodie", "Motion Flex Tights", "Pro Training Tracksuit"], "mrp_range": (2499, 5999), "cogs_ratio": 0.32, "elasticity_base": -2.1},
        {"category": "Accessories & Gear", "skus": ["Apex Utility Duffel 30L", "Ergonomic Sports Bottle", "Ventilated Run Cap"], "mrp_range": (799, 2999), "cogs_ratio": 0.28, "elasticity_base": -2.6}
    ]
    
    discount_tiers = [0, 10, 15, 20, 30, 40, 50]
    records = []
    
    for cat in categories:
        for sku in cat["skus"]:
            mrp = random.randint(cat["mrp_range"][0] // 500, cat["mrp_range"][1] // 500) * 500 - 1
            cogs = round(mrp * cat["cogs_ratio"], 2)
            base_weekly_sales = random.randint(120, 280)
            initial_stock = random.randint(1500, 3500)
            
            for disc in discount_tiers:
                price_ratio = (100 - disc) / 100.0
                elasticity = cat["elasticity_base"] + random.uniform(-0.15, 0.15)
                lift = (price_ratio ** elasticity)
                
                simulated_weekly_units = int(base_weekly_sales * lift * random.uniform(0.95, 1.05))
                effective_price = round(mrp * price_ratio, 2)
                revenue = round(simulated_weekly_units * effective_price, 2)
                gross_margin = round(revenue - (simulated_weekly_units * cogs), 2)
                margin_pct = round((gross_margin / revenue) * 100, 2) if revenue > 0 else 0
                
                units_sold_cycle = min(simulated_weekly_units * 4, initial_stock)
                sell_through_rate = round((units_sold_cycle / initial_stock) * 100, 2)
                
                records.append({
                    "category": cat["category"],
                    "sku_name": sku,
                    "mrp": mrp,
                    "cogs": cogs,
                    "discount_pct": disc,
                    "effective_price": effective_price,
                    "weekly_units_sold": simulated_weekly_units,
                    "initial_stock": initial_stock,
                    "projected_revenue": revenue,
                    "gross_margin_inr": gross_margin,
                    "gross_margin_pct": margin_pct,
                    "sell_through_rate_pct": sell_through_rate,
                    "price_elasticity": round(elasticity, 2)
                })
                
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    headers = [
        "category", "sku_name", "mrp", "cogs", "discount_pct", "effective_price",
        "weekly_units_sold", "initial_stock", "projected_revenue", "gross_margin_inr",
        "gross_margin_pct", "sell_through_rate_pct", "price_elasticity"
    ]
    
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Generated {len(records)} trading pricing records written to {output_path}")

if __name__ == "__main__":
    generate_trading_data()
