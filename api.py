from flask import Flask, request, jsonify, Response
from sqlalchemy import create_engine, text
import pandas as pd
import os
from datetime import datetime

api = Flask(__name__)

# Database Connection
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'database.db')

DB_URL = f"sqlite:///{db_path}"
engine = create_engine(DB_URL, echo=False)

# Read table and return JSON
def read_table(table_name, date_column=None, sort_by=None):
    start_str = request.args.get('start')
    end_str = request.args.get('end')

    params = {}
    filters = []

    query = f"SELECT * FROM {table_name}"

    # Date filters
    if start_str and date_column:
        try:
            params['start'] = datetime.strptime(start_str, '%Y-%m-%d').date()
            filters.append(f"{date_column} >= :start")
        except ValueError:
            return jsonify({"error": "Invalid start date. Use YYYY-MM-DD."}), 400

    if end_str and date_column:
        try:
            params['end'] = datetime.strptime(end_str, '%Y-%m-%d').date()
            filters.append(f"{date_column} <= :end")
        except ValueError:
            return jsonify({"error": "Invalid end date. Use YYYY-MM-DD."}), 400

    if filters:
        query += " WHERE " + " AND ".join(filters)

    if sort_by:
        query += f" ORDER BY {sort_by}"

    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(query), connection, params=params)

        json_data = df.to_json(orient='records', date_format='iso')
        return Response(json_data, mimetype='application/json')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Dimension Endpoints
@api.route("/api/dim/dates")
def get_dates():
    return read_table("dimension_dates", date_column="date", sort_by="date")

@api.route("/api/dim/branches")
def get_branches():
    return read_table("dimension_branches", sort_by="branch_id")

@api.route("/api/dim/materials")
def get_materials():
    return read_table("dimension_materials", sort_by="material_id")

# Fact Endpoints (with date filters)
@api.route("/api/fact/purchases")
def get_purchases():
    return read_table("fact_purchases", date_column="date")

@api.route("/api/fact/sales")
def get_sales():
    return read_table("fact_sales", date_column="date")

# Health Check
@api.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "database_path": db_path
    })

# Run the Api
if __name__ == "__main__":
    api.run(host="0.0.0.0", port=5000, debug=True)