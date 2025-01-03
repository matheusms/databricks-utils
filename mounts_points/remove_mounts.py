# Databricks notebook source
# MAGIC %md
# MAGIC # Deleta os mounts da lista informada

# COMMAND ----------

#lista de mounts a serem deletados
mounts = ['/mnt/landed', '/mnt/raw', '/mnt/silver', '/mnt/gold', '/mnt/imported', '/mnt/layouts']

#lista todos os mounts
mount_points = []
for mount_info in dbutils.fs.mounts():
    mount_points.append(mount_info.mountPoint)

#deleta o mount listado se ele existir
for mount in mounts:
    if mount in mount_points:
        dbutils.fs.unmount(mount)
        print(f"deletado {mount}")

# COMMAND ----------

# MAGIC %md
# MAGIC # Deletando todos os mounts do ambiente