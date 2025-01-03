# Databricks notebook source
# DBTITLE 1,Lista todos os mnt
mount_points = []
for mount_info in dbutils.fs.mounts():
    mount_points.append(mount_info.mountPoint)

# COMMAND ----------

storage_account = "<storageAccountName>"
secret_scope = "<keyvault-name>"
secret_key = "<adb-secret-name>"
client_id = "0000000-000000-000000-000000-000000000"

# COMMAND ----------

dbutils.secrets.listScopes()

# COMMAND ----------

storage_account_key = dbutils.secrets.get(scope = secret_scope, key = secret_key)

# COMMAND ----------

print("Criação dos mounts para o storage: ", storage_account)

containers_list = ['analysis', 'landed', 'raw', 'silver', 'gold', 'layouts', 'imported', 'staging']

for container in containers_list:
    mount_point = f"/mnt/{container}"
    print("mnt: ", mount_point)
    if mount_point not in mount_points:

        # autenticação na azure para criação dos mounts
        configs = {"fs.azure.account.auth.type": "OAuth",
              "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
              "fs.azure.account.oauth2.client.id": client_id,
              "fs.azure.account.oauth2.client.secret": storage_account_key,
              "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/889ece36-85c6-46c8-a7bd-b9c04d57ddb2/oauth2/token"}
        print("")

        # criação dos mounts com base no container
        dbutils.fs.mount(
          source=f"abfss://{container}@{storage_account}.dfs.core.windows.net/",
          mount_point = mount_point,
          extra_configs=configs
        )