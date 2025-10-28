import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..', 'database.db')
schema_path = os.path.join(script_dir, 'schema.sql')

# Remove existing database
if os.path.exists(db_path):
    try:
        os.remove(db_path)
    except PermissionError:
        print(f"Could not remove existing database {db_path}, it might be in use. Please close any database connections and try again.")
        exit(1)

# Execute schema
with sqlite3.connect(db_path) as conn:
    with open(schema_path, 'r') as f:
        schema = f.read()
    conn.executescript(schema)

print("Database initialized with schema.")