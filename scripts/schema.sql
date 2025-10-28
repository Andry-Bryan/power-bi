-- DIMENSION TABLES

-- Dates
CREATE TABLE dimension_dates (
    date_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE
);

-- Branches
CREATE TABLE dimension_branches (
    branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    state CHAR(2) NOT NULL,
    latitude REAL,
    longitude REAL
);

-- Materials
CREATE TABLE dimension_materials (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL
);

-- FACT TABLES

-- Purchases
CREATE TABLE fact_purchases (
    purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL, -- For filtering in the API request
    date_id INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    tons_bought REAL NOT NULL,
    price_per_ton REAL NOT NULL,
    FOREIGN KEY(date_id) REFERENCES dimension_dates(date_id),
    FOREIGN KEY(branch_id) REFERENCES dimension_branches(branch_id),
    FOREIGN KEY(material_id) REFERENCES dimension_materials(material_id)
);

-- Sales
CREATE TABLE fact_sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL, -- For filtering in the API request
    date_id INTEGER NOT NULL,
    branch_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    tons_sold REAL NOT NULL,
    price_per_ton REAL NOT NULL,
    FOREIGN KEY(date_id) REFERENCES dimension_dates(date_id),
    FOREIGN KEY(branch_id) REFERENCES dimension_branches(branch_id),
    FOREIGN KEY(material_id) REFERENCES dimension_materials(material_id)
);