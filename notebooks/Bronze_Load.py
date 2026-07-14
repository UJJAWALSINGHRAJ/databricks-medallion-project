# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS us_project_catalog;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE SCHEMA IF NOT EXISTS us_project_catalog.us_brons_schema;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE VOLUME IF NOT EXISTS us_project_catalog.us_brons_schema.bronze_volume;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW CATALOGS;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS us_project_catalog.us_brons_schema;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN us_project_catalog;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES IN us_project_catalog.us_brons_schema;

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG us_project_catalog;

# COMMAND ----------

# MAGIC %sql
# MAGIC USE SCHEMA us_brons_schema;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES;

# COMMAND ----------

display(dbutils.fs.ls("/Volumes/us_project_catalog/us_brons_schema/bronze_volume"))

# COMMAND ----------

display(dbutils.fs.ls("/Volumes/us_project_catalog/us_brons_schema/bronze_volume"))

# COMMAND ----------

import zipfile
import os
import shutil

volume_path = "/Volumes/us_project_catalog/us_brons_schema/bronze_volume"
zip_file = volume_path + "/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2010_1.zip"

extract_path = "/tmp/flight_data"

# Purana folder delete
if os.path.exists(extract_path):
    shutil.rmtree(extract_path)

os.makedirs(extract_path)

# ZIP extract
with zipfile.ZipFile(zip_file, "r") as zip_ref:
    zip_ref.extractall(extract_path)

print("ZIP Extracted Successfully")

# COMMAND ----------

import glob

csv_files = glob.glob("/tmp/flight_data/*.csv")

print(csv_files)

# COMMAND ----------

import zipfile
import os

volume_path = "/Volumes/us_project_catalog/us_brons_schema/bronze_volume"

zip_file = f"{volume_path}/On_Time_Reporting_Carrier_On_Time_Performance_1987_present_2010_1.zip"

extract_path = f"{volume_path}/extracted"

os.makedirs(extract_path, exist_ok=True)

with zipfile.ZipFile(zip_file, "r") as zip_ref:
    zip_ref.extractall(extract_path)

print("ZIP extracted successfully.")

# COMMAND ----------

import os

files = os.listdir("/Volumes/us_project_catalog/us_brons_schema/bronze_volume/extracted")

print(files)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

display(df.limit(5))

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit
import os

csv_file = "/Volumes/us_project_catalog/us_brons_schema/bronze_volume/extracted/On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2010_1.csv"

df = df.withColumn("current_time", current_timestamp()) \
       .withColumn("file_name", lit(os.path.basename(csv_file)))

display(df.select("Year","FlightDate","Origin","Dest","current_time","file_name"))

# COMMAND ----------

output_path = "/Volumes/us_project_catalog/us_brons_schema/bronze_volume/bronze_output"

df.write \
    .format("delta") \
    .mode("overwrite") \
    .save(output_path)

print("✅ Data saved successfully to Bronze Volume.")

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES IN us_project_catalog.us_brons_schema;

# COMMAND ----------

display(dbutils.fs.ls("/Volumes/us_project_catalog/us_brons_schema/bronze_volume/bronze_output"))

# COMMAND ----------

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("us_project_catalog.us_brons_schema.flight_data")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC SELECT
# MAGIC     Year,
# MAGIC     FlightDate,
# MAGIC     Origin,
# MAGIC     Dest,
# MAGIC     current_time,
# MAGIC     file_name
# MAGIC FROM us_project_catalog.us_brons_schema.flight_data
# MAGIC LIMIT 10;