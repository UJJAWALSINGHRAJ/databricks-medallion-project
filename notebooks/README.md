# Databricks Notebooks
# Databricks Medallion Architecture Project

## Overview
This project demonstrates the implementation of the Medallion Architecture using Databricks, Unity Catalog, Delta Lake, PySpark, and SQL.

## Bronze Layer
- Created Unity Catalog
- Created Schema
- Created Volume
- Uploaded flight dataset
- Extracted ZIP file
- Loaded CSV into Spark DataFrame
- Added `current_time` column
- Added `file_name` column
- Saved data as Delta Table

## Technologies Used
- Databricks
- Apache Spark
- PySpark
- SQL
- Unity Catalog
- Delta Lake

## Repository Structure

```
databricks-medallion-project
│
├── notebooks
│   ├── Bronze_Load.py
│   ├── Silver_Load.py
│   └── Gold_Load.py
│
└── README.md
```
