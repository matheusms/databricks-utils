# Databricks notebook source
# MAGIC %md
# MAGIC # Verifica as tabelas que estão sendo atualizadas no Hive Metastore pelo ADF

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, expr
from pyspark.sql.functions import col

# COMMAND ----------

def check_table_history_for_adf(catalog_name):
    schemas = spark.sql(f"SHOW SCHEMAS IN {catalog_name}").collect()
    results = []

    for schema in schemas:
        schema_name = schema['databaseName']

        tables = spark.sql(f"SHOW TABLES IN {catalog_name}.{schema_name}").collect()

        for table in tables:
            table_name = table['tableName']
            full_table_name = f"{catalog_name}.{schema_name}.{table_name}"

            try:
                history = spark.sql(f"DESCRIBE HISTORY {full_table_name}")

                if 'job' in history.columns and 'jobName' in history.select('job.*').columns:
                    adf_jobs = history.filter(col("job.jobName").like("%ADF%"))

                    if adf_jobs.count() > 0:
                        latest_adf_job = adf_jobs.orderBy(col("timestamp").desc()).first()
                        results.append({
                            "catalog": catalog_name,
                            "schema": schema_name,
                            "table": table_name,
                            "has_adf_job": True,
                            "latest_adf_timestamp": latest_adf_job["timestamp"]
                        })
                    else:
                        results.append({
                            "catalog": catalog_name,
                            "schema": schema_name,
                            "table": table_name,
                            "has_adf_job": False,
                            "latest_adf_timestamp": None
                        })
                else:
                    print(f"Warning: 'job'.'jobName' column not found in history for {full_table_name}")

            except Exception as e:
                print(f"Error processing {full_table_name}: {str(e)}")

    return spark.createDataFrame(results)

catalog_name = "hive_metastore"
result_df = check_table_history_for_adf(catalog_name)

# COMMAND ----------


#filtra o intervalo de data desejado
filtered_result_df = result_df.filter((col("has_adf_job") == True) & (col("latest_adf_timestamp") > expr("current_timestamp() - interval 3 days")))
display(filtered_result_df)
