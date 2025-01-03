# Databricks notebook source
# MAGIC %pip install tqdm==4.66.5

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from typing import List, Tuple
from tqdm import tqdm

# COMMAND ----------

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

# COMMAND ----------

all_tables_to_clone = [
    ('hive_metastore', 'DATABASE1', 'TABLE_1'),
    ('hive_metastore', 'DATABASE2', 'TABLE_2')
    ]

target_catalog = f"YOUR_CATALOG_NAME"

# COMMAND ----------

#gera os comandos de clone em uma lista
clone_commands = generate_clone_commands(all_tables_to_clone, target_catalog)
execute_clone_commands(clone_commands, dry_run=False)
