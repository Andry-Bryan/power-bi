from sqlalchemy import create_engine
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..', 'database.db')
DB_URL = f"sqlite:///{db_path}"
engine = create_engine(DB_URL)

data_dir = os.path.join(script_dir, '..', 'data')
csv_paths = {
    'dates': os.path.join(data_dir, 'dates.csv'),
    'branches': os.path.join(data_dir, 'branches.csv'),
    'materials': os.path.join(data_dir, 'materials.csv'),
    'purchases': os.path.join(data_dir, 'purchases.csv'),
    'sales': os.path.join(data_dir, 'sales.csv')
}

# Load Dimensions
for table, path in csv_paths.items():
    df = pd.read_csv(path)
    df.to_sql(f'dimension_{table}', engine, if_exists='replace', index=False)

# Load Facts
for table in ['purchases', 'sales']:
    df = pd.read_csv(csv_paths[table])
    df.to_sql(f'fact_{table}', engine, if_exists='replace', index=False)
