import random
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "live_sales.csv"

products = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard"]
regions = ["North", "South", "East", "West"]

def generate_data():
    return {
        "order_id": random.randint(1000, 9999),
        "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "product": random.choice(products),
        "region": random.choice(regions),
        "sales": random.randint(500, 2500),
        "quantity": random.randint(1, 5)
    }

def init_file():
    if not DATA_PATH.exists():
        df = pd.DataFrame(columns=["order_id", "order_date", "product", "region", "sales", "quantity"])
        df.to_csv(DATA_PATH, index=False)

def run_stream():
    init_file()
    while True:
        row = generate_data()
        pd.DataFrame([row]).to_csv(DATA_PATH, mode="a", header=False, index=False)
        print("New row added:", row)
        time.sleep(5)

if __name__ == "__main__":
    run_stream()