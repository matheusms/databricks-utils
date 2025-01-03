# Databricks notebook source
# MAGIC %md
# MAGIC ## Listar pontos de montagem disponíveis
# MAGIC #### Nota: Como precisamos usar dbutils.fs.mounts(), a célula abaixo precisa ser executada em um cluster não-UC

# COMMAND ----------

dbutils.fs.mounts()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Contar número de pontos de montagem
# MAGIC #### Nota: Como precisamos usar dbutils.fs.mounts(), a célula abaixo precisa ser executada em um cluster não-UC

# COMMAND ----------

mounts = dbutils.fs.mounts()
distinct_mount_points = len(set([mount.mountPoint for mount in mounts]))
distinct_mount_points

# COMMAND ----------

# MAGIC %md
# MAGIC ## Listar contêineres existentes e criar locais externos
# MAGIC #### Nota: Como precisamos usar dbutils.fs.mounts(), a célula abaixo precisa ser executada em um cluster não-UC

# COMMAND ----------

mounts = dbutils.fs.mounts()
containers = set()
sql_commands = []
for mount in mounts:
    source = mount.source
    location_name = source.split('@')[0].split('//')[-1]  # Extracting the container name
    containers.add(location_name)
    storage_credential = f"{location_name}_credential"  # Assuming a naming convention for storage credentials
    sql_command = f"CREATE EXTERNAL LOCATION {location_name} URL '{source}' WITH STORAGE CREDENTIAL {storage_credential}"
    sql_commands.append(sql_command)

sorted_containers = sorted(containers)
for container in sorted_containers:
    print(container)
# for command in sql_commands:
    # display(command)
