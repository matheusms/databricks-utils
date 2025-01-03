# Databricks notebook source
# DBTITLE 1,Criando Databricks Consumer
# MAGIC %sql
# MAGIC --CREATE RECIPIENT IF NOT EXISTS <nome_receptor> USING ID 'id_do_receptor' COMMENT 'Inserir Comentário....'

# COMMAND ----------

# DBTITLE 1,Criando Consumer não Databricks
# MAGIC %sql
# MAGIC CREATE RECIPIENT IF NOT EXISTS <nome_receptor> COMMENT 'Tabelas serão utilizadas por robôs criados através da área Análises e Informações...'

# COMMAND ----------

# DBTITLE 1,Alterando Owner recipient
# MAGIC %sql
# MAGIC ALTER RECIPIENT <nome_receptor> OWNER TO `<nome_grupoAcesso>`

# COMMAND ----------

# DBTITLE 1,Criando um Data Share
# MAGIC %sql
# MAGIC CREATE SHARE IF NOT EXISTS <nome_share> COMMENT 'Compartilhamento criado para a área Análises e Informações...'

# COMMAND ----------

# DBTITLE 1,Alterando Owner
# MAGIC %sql
# MAGIC ALTER SHARE <nome_share> OWNER TO `<nome_grupoAcesso>`

# COMMAND ----------

# DBTITLE 1,Add Tabelas no Share
# MAGIC %sql
# MAGIC ALTER SHARE <nome_share> ADD TABLE <your_catalog.schema.table>

# COMMAND ----------

# DBTITLE 1,Removendo tabela do Share
# MAGIC %sql
# MAGIC --ALTER SHARE <nome_share> REMOVE TABLE <your_catalog.schema.table>

# COMMAND ----------

# DBTITLE 1,Visualizar as tabelas no Share
# MAGIC %sql
# MAGIC SHOW ALL IN SHARE <nome_share>

# COMMAND ----------

# DBTITLE 1,Grant no  Share para os Receptores
# MAGIC %sql
# MAGIC GRANT SELECT ON SHARE <nome_share> TO RECIPIENT <nome_receptor>

# COMMAND ----------

# DBTITLE 1,Revogar acesso ao Share
# MAGIC %sql
# MAGIC --REVOKE SELECT ON SHARE <nome_share> FROM RECIPIENT <nome_receptor>;
