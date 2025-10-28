import pandas as pd
import random
from datetime import date, timedelta
import os
import calendar

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
os.makedirs(data_dir, exist_ok=True)

dates_csv_path = os.path.join(data_dir, 'dates.csv')
branches_csv_path = os.path.join(data_dir, 'branches.csv')
materials_csv_path = os.path.join(data_dir, 'materials.csv')
purchases_csv_path = os.path.join(data_dir, 'purchases.csv')
sales_csv_path = os.path.join(data_dir, 'sales.csv')

N_DAYS = 366
start_date = date(2024, 1, 1)

# Generate Dates
rows = []
for d in range(N_DAYS):
    current_date = start_date + timedelta(days=d)
    row = {
        "date_id": d + 1,
        "date": current_date
    }
    rows.append(row)

df_dates = pd.DataFrame(rows)
df_dates.to_csv(dates_csv_path, index=False)

# Generate Branches
branches = [
    {"branch_id": 1, "state": "RJ", "latitude": -22.91, "longitude": -43.17},
    {"branch_id": 2, "state": "MG", "latitude": -19.92, "longitude": -43.93},
    {"branch_id": 3, "state": "ES", "latitude": -20.33, "longitude": -40.34},
]
df_branches = pd.DataFrame(branches)
df_branches.to_csv(branches_csv_path, index=False)

# Generate Materials
materials = [
    {"material_id": 1, "category": "metal"},
    {"material_id": 2, "category": "plastic"},
    {"material_id": 3, "category": "paper"},
]
df_materials = pd.DataFrame(materials)
df_materials.to_csv(materials_csv_path, index=False)

# Configs
purchases_config = {
    'tons_bought': {
        'RJ': {'metal': (0, 10), 'plastic': (0, 4), 'paper': (0, 2)},
        'MG': {'metal': (0, 6), 'plastic': (0, 3), 'paper': (0, 2)},
        'ES': {'metal': (0, 5), 'plastic': (0, 2), 'paper': (0, 1)},
    },
    'price_per_ton': {
        'RJ': {'metal': (900, 1100), 'plastic': (600, 800), 'paper': (400, 600)},
        'MG': {'metal': (900, 1100), 'plastic': (600, 800), 'paper': (400, 600)},
        'ES': {'metal': (900, 1100), 'plastic': (600, 800), 'paper': (400, 600)},
    }
}

sales_config = {
    'tons_sold': {
        'RJ': {'metal': (0, 8), 'plastic': (0, 3), 'paper': (0, 1.5)},
        'MG': {'metal': (0, 5), 'plastic': (0, 2), 'paper': (0, 1.3)},
        'ES': {'metal': (0, 4), 'plastic': (0, 1.5), 'paper': (0, 0.7)},
    },
    'price_per_ton': {
        'RJ': {'metal': (1400, 1800), 'plastic': (1000, 1300), 'paper': (700, 900)},
        'MG': {'metal': (1400, 1800), 'plastic': (1000, 1300), 'paper': (700, 900)},
        'ES': {'metal': (1400, 1800), 'plastic': (1000, 1300), 'paper': (700, 900)},
    }
}

# Generate Facts
def generate_facts(file_path, config):
    rows = []
    columns = list(config.keys())
    for d in range(N_DAYS):
        current_date = start_date + timedelta(days=d)
        date_id = d + 1
        month = current_date.month
        for branch in branches:
            for material in materials:
                row = {
                    "date_id": date_id,
                    "date": current_date,
                    "branch_id": branch['branch_id'],
                    "material_id": material['material_id'],
                }
                for col in columns:
                    min_val, max_val = config[col][branch['state']][material['category']]
                    base_value = random.uniform(min_val, max_val)
                    
                    # monthly trends
                    growth_factor = (1 + 0.05) ** (month - 1)
                    noise = 1 + random.uniform(-0.1, 0.1)
                    
                    final_value = base_value * growth_factor * noise
                    row[col] = round(final_value, 2)
                rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(file_path, index=False)

generate_facts(purchases_csv_path, purchases_config)
generate_facts(sales_csv_path, sales_config)