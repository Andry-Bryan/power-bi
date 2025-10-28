# Project Documentation

## 1. Overview

This project provides a Flask-based API for a Power BI dashboard, using a synthetically generated dataset that mimics a recycling business. It includes data on branches, materials, purchases, and sales.

## 2. Folder Structure

```
power-bi/
├── api.py                     # Main Flask API file
├── database.db                # SQLite database file
├── requirements.txt           # Python dependencies
├── .venv/                     # Virtual environment files
├── data/                      # CSV files with synthetic data
│   ├── branches.csv
│   ├── dates.csv
│   ├── materials.csv
│   ├── purchases.csv
│   └── sales.csv
├── docs/                      # Documentation files
│   ├── documentation.md
│   └── setup_instructions.md
├── powerbi/                   # Power BI dashboard file
│   └── dashboard.pbix
└── scripts/                   # Scripts for database and data management
    ├── create_db.py
    ├── generate_data.py
    ├── load_to_db.py
    ├── schema.sql
    └── setup_database.py
```

## 3. Setup

For setup and execution instructions, refer to `setup_instructions.md`.

## 4. Database Schema

The database schema is defined in `scripts/schema.sql`. It follows a star schema with three dimension tables and two fact tables.

### 4.1. Dimension Tables

-   **`dimension_dates`**: Stores date-related information.
    -   `date_id`: Primary key for date dimension.
    -   `date`: The specific date in `YYYY-MM-DD` format.

-   **`dimension_branches`**: Contains information about each branch.
    -   `branch_id`: Primary key for branch dimension.
    -   `state`: The state where the branch is located (e.g., "RJ").
    -   `latitude`: The geographical latitude of the branch.
    -   `longitude`: The geographical longitude of the branch.

-   **`dimension_materials`**: Describes the different types of recyclable materials.
    -   `material_id`: Primary key for material dimension.
    -   `category`: The primary classification of the material (e.g., "metal").

### 4.2. Fact Tables

-   **`fact_purchases`**: Records all material purchase transactions.
    -   `purchase_id`: Primary key for each purchase transaction.
    -   `date`: Transaction date, for direct querying.
    -   `date_id`: Foreign key to `dimension_dates`, linking to the date dimension.
    -   `branch_id`: Foreign key to `dimension_branches`, linking to the branch where the purchase occurred.
    -   `material_id`: Foreign key to `dimension_materials`, linking to the material purchased.
    -   `tons_bought`: The weight of the material purchased, in tons.
    -   `price_per_ton`: The cost for one ton of the specified material.

-   **`fact_sales`**: Records all material sales transactions.
    -   `sale_id`: Primary key for each sale transaction.
    -   `date`: Transaction date, for direct querying.
    -   `date_id`: Foreign key to `dimension_dates`, linking to the date dimension.
    -   `branch_id`: Foreign key to `dimension_branches`, linking to the branch where the sale occurred.
    -   `material_id`: Foreign key to `dimension_materials`, linking to the material sold.
    -   `tons_sold`: The weight of the material sold, in tons.
    -   `price_per_ton`: The revenue for one ton of the specified material.

## 5. Data Generation

The `scripts/generate_data.py` script creates the synthetic dataset, generating CSV files stored in the `data/` directory. The data spans the full year of 2024 and includes simulated monthly trends and random variations.

## 6. API Endpoints

The API is defined in `api.py` and exposes the following endpoints:

### 6.1. Dimensions

-   **GET `/api/dim/dates`**: Retrieves all dates.
-   **GET `/api/dim/branches`**: Retrieves all branches.
-   **GET `/api/dim/materials`**: Retrieves all materials.

### 6.2. Facts

The fact endpoints return transactional data and can be filtered by a date range. This is done by providing `start` and `end` query parameters in `YYYY-MM-DD` format. If no parameters are provided, they will return all data.

-   **GET `/api/fact/purchases`**: Retrieves purchase records.
    -   **Example**: `/api/fact/purchases?start=2024-01-01&end=2024-01-31`
-   **GET `/api/fact/sales`**: Retrieves sales records.
    -   **Example**: `/api/fact/sales?start=2024-06-01`

### 6.3. Health Check

-   **GET `/api/health`**: Returns API status and database path.

## 7. Scripts

The `scripts/` directory contains helper scripts for database management:

-   **`create_db.py`**: Creates the database from `schema.sql`.
-   **`generate_data.py`**: Generates the synthetic data.
-   **`load_to_db.py`**: Loads CSV data into the database.
fs/
-   **`schema.sql`**: Defines the database table structures.
-   **`setup_database.py`**: Executes all scripts in the correct order to set up and populate the database.
