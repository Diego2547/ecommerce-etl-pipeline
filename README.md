# Automated E-commerce ETL Pipeline

## Overview

This project is a Python-based ETL pipeline that extracts sample e-commerce product data from the DummyJSON API, transforms it using pandas, and stores the resulting datasets in SQLite.

Its goal is to prepare structured product data for further analysis with SQL and business intelligence tools such as Power BI.

The project includes a scheduling script that coordinates the ETL and transformation processes and prevents the second stage from running if the first stage fails.

## Technologies Used

- **Python:** Pipeline development and orchestration
- **Requests:** API data extraction
- **Pandas:** Data cleaning and transformation
- **SQLite:** Relational data storage
- **Schedule:** Periodic execution while the scheduler is running
- **Logging:** Execution monitoring and error tracking

## ETL Workflow

1. **Extract:** Retrieve product data from the DummyJSON API.
2. **Process:** Organize products, images, and tags into separate datasets.
3. **Load:** Store the datasets in SQLite.
4. **Transform:** Clean product data, calculate discounted prices, and classify product ratings.
5. **Export:** Save the cleaned dataset as CSV and in SQLite.
6. **Automate:** Coordinate script execution and stop subsequent stages when a failure is reported.

## Project Structure

```text
ecommerce-etl-pipeline/
├── ETL/
│   ├── ETL.py
│   └── Transform.py
├── automation/
│   └── automation.py
├── results/
│   ├── products.csv
│   └── products_clean.csv
├── .gitignore
├── README.md
└── requirements.txt
```

The SQLite database and execution logs are generated locally and excluded from version control.

## Installation

Clone the repository:

```bash
git clone https://github.com/Diego2547/ecommerce-etl-pipeline.git
cd ecommerce-etl-pipeline
```

Install the required Python packages:

```bash
python -m pip install -r requirements.txt
```

## Usage

To run the extraction and loading process:

```bash
python ETL/ETL.py
```

To run the subsequent data transformation:

```bash
python ETL/Transform.py
```

To run the automated pipeline:

```bash
python automation/automation.py
```

The automation script coordinates both stages and only executes `Transform.py` when `ETL.py` finishes successfully.

**Scheduling note:** When periodic scheduling is enabled, the scheduler must remain running. It does not execute tasks while the computer or process is turned off.

## Future Improvements

- Add SQL queries to analyze product pricing, discounts, and ratings.
- Improve configuration and error handling.
- Add automated tests and data-quality checks.
- Explore dashboards using the prepared data.
