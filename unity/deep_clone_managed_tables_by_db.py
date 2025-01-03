# Databricks notebook source
# MAGIC %pip install tqdm==4.66.5

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from typing import List, Tuple
from tqdm import tqdm

def get_tables_in_schema(schema: str) -> List[Tuple[str, str, str]]:
    """
    Retrieve all tables in a given schema.
    
    :param schema: Schema name
    :return: List of tuples (catalog, schema, table_name)
    """
    print(f"\nRetrieving tables in schema: {schema}")
    tables = spark.sql(f"SHOW TABLES IN {schema}").select("database", "tableName").collect()
    return [(schema.split('.')[0], schema.split('.')[1], table.tableName) for table in tables]

def generate_clone_commands(tables: List[Tuple[str, str, str]], target_catalog: str) -> List[str]:
    """
    Generate DEEP CLONE commands for specified tables using a simpler syntax.
    
    :param tables: List of tuples (source_catalog, source_schema, table_name)
    :param target_catalog: Name of the target Unity Catalog
    :return: List of CLONE SQL commands
    """
    print(f"\nGenerating clone commands for target catalog: {target_catalog}")
    commands = []
    for source_catalog, source_schema, table_name in tables:
        source_table = f"{source_catalog}.{source_schema}.{table_name}"
        target_table = f"{target_catalog}.{source_schema}.{table_name}"
        
        clone_command = f"CREATE OR REPLACE TABLE {target_table} DEEP CLONE {source_table}"
        change_table_owner_command = f"ALTER TABLE {target_table} OWNER TO `uc_owner`"
        commands.append(clone_command)
        commands.append(change_table_owner_command)
    return commands

def execute_clone_commands(commands: List[str], dry_run: bool = True) -> None:
    """
    Execute or print the clone commands.
    
    :param commands: List of SQL commands to execute
    :param dry_run: If True, only print commands. If False, execute them.
    """
    for command in tqdm(commands, desc="Executing clone commands"):
        if dry_run:
            print(f"\n[DRY RUN] Would execute: {command}")
        else:
            print(f"\nExecuting: {command}")
            spark.sql(command)

# List of schemas to clone
schemas_to_clone = [
    "hive_metastore.DATABASE1",
    "hive_metastore.DATABASE2",
]

target_catalog = f"YOUR_CATALOG_NAME"

all_tables_to_clone = []
for schema in tqdm(schemas_to_clone, desc="Processing schemas"):
    print(f"\nCreating schema if not exists: {target_catalog}.{schema.split('.')[1]}")

    #cria o schema se ele nao existir
    execute_clone_commands([f"CREATE SCHEMA IF NOT EXISTS {target_catalog}.{schema.split('.')[1]}"], dry_run=False)

    #altera o owner do schema
    execute_clone_commands([f"ALTER SCHEMA {target_catalog}.{schema.split('.')[1]} OWNER TO `uc_owner`"], dry_run=False)

    #gera as tabelas que serão clonadas
    all_tables_to_clone.extend(get_tables_in_schema(schema))

#gera os comandos de clone em uma lista
clone_commands = generate_clone_commands(all_tables_to_clone, target_catalog)
execute_clone_commands(clone_commands, dry_run=False)
