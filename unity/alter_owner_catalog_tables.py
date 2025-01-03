# Databricks notebook source
# MAGIC %md
# MAGIC # Notebook: Padronização de Owners no Catálogo
# MAGIC
# MAGIC Este notebook verifica e ajusta os *owners* dos *schemas* e tabelas no catálogo para garantir que todos estejam atribuídos ao grupo `uc_owner`.
# MAGIC
# MAGIC ## Fluxo do Notebook
# MAGIC
# MAGIC 1. **Schemas**: Percorre os *schemas* do catálogo e, se algum tiver *owner* diferente de `uc_owner`, atualiza-o para `uc_owner`.
# MAGIC 2. **Tabelas**: Em seguida, verifica as tabelas dentro de cada *schema* e realiza a mesma atualização, caso necessário.

# COMMAND ----------

# MAGIC %pip install tqdm==4.66.5

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

from tqdm import tqdm

# COMMAND ----------

# MAGIC %md
# MAGIC ## Altera o Owner dos Schemas do Catálogo para `uc_owner`

# COMMAND ----------

# DBTITLE 1,Altera o owner dos Schemas
#extrai com dados de todas as tabelas da base as tabelas com o owner errado
df_schemas = spark.sql(f"""
    SELECT catalog_name, schema_name, schema_owner 
    FROM YOUR_CATALOG_NAME.information_schema.schemata
    WHERE schema_owner != 'uc_owner' 
    AND schema_name != 'information_schema'
""")

#remove os schemas duplicados
df_schemas_distinct = df_schemas.select("catalog_name", "schema_name").distinct()
print("Quantidade de Tabelas que serão alteradas: ", df_schemas_distinct.count())

if df_schemas_distinct.limit(1).count() > 0:
    print("Tabelas que serão alteradas:")
    display(df_schemas_distinct)

    lista_erro = []


    print("Iniciando alteração de owner das tabelas.")
    for row in tqdm(df_schemas_distinct.select("catalog_name", "schema_name").distinct().collect(), desc="Alterando owner dos schemas."):
        # Dados do usuário
        t_catalog = row['catalog_name']
        t_schema = row['schema_name']

        try:
            spark.sql(f"ALTER SCHEMA {t_catalog}.{t_schema} OWNER TO `uc_owner`")
            # print(f"ALTER SCHEMA {t_catalog}.{t_schema} OWNER TO `uc_owner`")
        
        except:
            lista_erro.append(f"ALTER SCHEMA {t_catalog}.{t_schema} OWNER TO `uc_owner`")
    print("Alteração de owner dos schemas finalizada.")
    if len(lista_erro) > 0:
        print("Falha ao alterar os donos dos schemas:")
        print(lista_erro)
else:
    print("Nenhuma schema encontrado.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Altera o Owner das tabelas do Catálogo para `uc_owner`

# COMMAND ----------

# DBTITLE 1,Altera o Owner das tabelas para o 'uc_owner'
#extrai com dados de todas as tabelas da base as tabelas com o owner errado
df_tables = spark.sql(f"""
    SELECT table_catalog, table_schema, table_name, table_owner 
    FROM YOUR_CATALOG_NAME.information_schema.tables
    WHERE table_owner != 'uc_owner' 
    AND table_schema != 'information_schema'
""")

print("Quantidade de Tabelas que serão alteradas: ", df_tables.count())

if df_tables.limit(1).count() > 0:
    print("Tabelas que serão alteradas:")
    display(df_tables)

    lista_erro = []


    print("Iniciando alteração de owner das tabelas.")
    for row in tqdm(df_tables.collect(), desc="Alterando o owner das tabelas."):
        # Dados do usuário
        t_catalog = row['table_catalog']
        t_schema = row['table_schema']
        t_name = row['table_name']

        try:
            spark.sql(f"ALTER TABLE {t_catalog}.{t_schema}.{t_name} OWNER TO `uc_owner`")
            # print(f"ALTER TABLE {t_catalog}.{t_schema}.{t_name} OWNER TO `uc_owner`")
        
        except:
            lista_erro.append(f"ALTER TABLE {t_catalog}.{t_schema}.{t_name} OWNER TO `uc_owner`")
    print("Alteração de owner das tabelas finalizada.")
    if len(lista_erro) > 0:
        print("Falha ao alterar os donos das tabelas:")
        print(lista_erro)
else:
    print("Nenhuma tabela encontrada.")
