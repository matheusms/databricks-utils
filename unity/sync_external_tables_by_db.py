# Databricks notebook source
# MAGIC %pip install tqdm==4.66.5

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from tqdm import tqdm

schema_list = [
    "hive_metastore.DATABASE1", 
    "hive_metastore.DATABASE2"
]
target_catalog = f"YOUR_CATALOG_NAME"

for schema_name in tqdm(schema_list, desc="Schemas"):
    target_schema = f"{target_catalog}.{schema_name.split('.')[1]}"
    
    #cria o schema no catalogo se não existir
    print(f"\nCreating schema if not exists: {target_schema}")
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {target_schema}")
    
    #altera o owner do schema
    print(f"\nAltering schema owner: {target_schema}")
    spark.sql(f"ALTER SCHEMA {target_schema} OWNER TO `uc_owner`")

    #realiza o sync da tabela
    print(f"\nSyncing schema: {target_schema} from {schema_name}")
    display(spark.sql(f"SYNC SCHEMA {target_schema} FROM {schema_name}"))    
    
    #realiza o for para passar nas tabelas do scheema
    tables = spark.sql(f"SHOW TABLES IN {target_schema}").select("tableName").collect()
    for table in tqdm(tables, desc=f"Tables in {target_schema}", leave=False):
        table_name = table.tableName

        #define o owner da tabela
        print(f"\nAltering table owner: {target_schema}.{table_name}")
        spark.sql(f"ALTER TABLE {target_schema}.{table_name} OWNER TO `uc_owner`")
