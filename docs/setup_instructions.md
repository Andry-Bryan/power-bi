# Setup Instructions

## 0. Install Python

## 1. Virtual Environment

Create the virtual environment. Run this command in the project root:
```bash
python -m venv .venv
```

Activate the Virtual Environment. Run this command in PowerShell:
```bash
.venv\Scripts\Activate.ps1
```

## 2. Install Dependencies

Install the required Python packages.
```bash
pip install -r requirements.txt
```

## 3. Setup Database with Synthetic Data

```bash
python scripts/setup_database.py
```

## 4. Run the Flask API

```bash
python api.py
```

The API will be available at `http://localhost:5000`.
