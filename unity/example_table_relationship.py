# Databricks notebook source
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Define the schema with id as non-nullable
schema_another = StructType([
    StructField("id", IntegerType(), nullable=False),
    StructField("department", StringType(), nullable=True)
])

# Create a sample DataFrame for another_table with the defined schema
data_another = [
    (1, "Engineering"),
    (2, "Marketing"),
    (3, "Sales")
]
df_another = spark.createDataFrame(data_another, schema=schema_another)

# Write the DataFrame to a table in Unity Catalog
df_another.write.saveAsTable("YOUR_CATALOG_NAME.default.another_table")

spark.sql("""
ALTER TABLE YOUR_CATALOG_NAME.default.another_table
ALTER COLUMN id SET NOT NULL
""")

# Add primary key constraint to another_table
spark.sql("""
ALTER TABLE YOUR_CATALOG_NAME.default.another_table
ADD CONSTRAINT pk_another_table PRIMARY KEY (id)
""")

# Display the another_table to verify
display(spark.sql("SELECT * FROM YOUR_CATALOG_NAME.default.another_table"))

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Define the schema for the sample_table
schema_sample = StructType([
    StructField("id", IntegerType(), nullable=False),
    StructField("name", StringType(), nullable=True),
    StructField("age", IntegerType(), nullable=True)
])

# Create a sample DataFrame with the defined schema
data = [
    (1, "Alice", 29),
    (2, "Bob", 35),
    (3, "Cathy", 28)
]
df = spark.createDataFrame(data, schema=schema_sample)

# Write the DataFrame to a table in Unity Catalog
df.write.saveAsTable("YOUR_CATALOG_NAME.default.sample_table")

spark.sql("""
ALTER TABLE YOUR_CATALOG_NAME.default.sample_table
ALTER COLUMN id SET NOT NULL
""")

# Add primary key and foreign key constraints
spark.sql("""
ALTER TABLE YOUR_CATALOG_NAME.default.sample_table
ADD CONSTRAINT pk_sample_table PRIMARY KEY (id)
""")

spark.sql("""
ALTER TABLE YOUR_CATALOG_NAME.default.sample_table
ADD CONSTRAINT fk_sample_table_another_table FOREIGN KEY (id) REFERENCES YOUR_CATALOG_NAME.default.another_table(id)
""")

# Display the table to verify
display(spark.sql("SELECT * FROM YOUR_CATALOG_NAME.default.sample_table"))

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Define the schema for the new_table
schema_new = StructType([
    StructField("id", IntegerType(), nullable=False),
    StructField("description", StringType(), nullable=True)
])

# Create a sample DataFrame with the defined schema
data_new = [
    (1, "Item A"),
    (2, "Item B"),
    (3, "Item C")
]
df_new = spark.createDataFrame(data_new, schema=schema_new)

# Write the DataFrame to a table in Unity Catalog
df_new.write.saveAsTable("YOUR_CATALOG_NAME.default.new_table")

spark.sql("""
ALTER TABLE YOUR_CATALOG_NAME.default.new_table
ALTER COLUMN id SET NOT NULL
""")

# Add primary key constraint to new_table
spark.sql("""
ALTER TABLE YOUR_CATALOG_NAME.default.new_table
ADD CONSTRAINT pk_new_table PRIMARY KEY (id)
""")

# Display the new_table to verify
display(spark.sql("SELECT * FROM YOUR_CATALOG_NAME.default.new_table"))
