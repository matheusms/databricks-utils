# Databricks notebook source
#incluir todas as tipagens necessárias ex: decimal(10,2), timestamp...
cast_types = {
  'string': 'VARCHAR(8000) COLLATE Latin1_General_100_BIN2_UTF8',
  'date': 'DATE',
  'double': 'float',
  'int': 'int'
}

database_raw_name = "db_name" #database que será usada para gerar o script de criação dos external table no synapse

spark.sql('use {}'.format(database_raw_name))

tables_raw = spark.sql('show tables').collect()

create_external_table = ""

for table_raw in tables_raw:
    
    table_raw_name = table_raw['tableName'] #aqui define a tabela, pode ser usado para apenas uma no schema (mas é necessário modificar o for)
    
    create_external_table += "CREATE EXTERNAL TABLE [dbo].[{}] ( \n ".format(table_raw_name)

    index = 0;

    columns = spark.sql('SHOW COLUMNS IN {}.{}'.format(database_raw_name, table_raw_name)).collect()
    
    for column in columns:
        column_name = column['col_name']

        detail = spark.sql('DESCRIBE {}.{} {}'.format(database_raw_name, table_raw_name, column_name)).collect()
        
        detail_column = spark.sql('DESCRIBE {}.{} {}'.format(database_raw_name, table_raw_name, column_name)).collect()
        detail_column_type = list(filter(lambda item: item.info_name == "data_type", detail_column))

        column_type = detail_column_type[0]['info_value']
        
        #monta o schema das colunas e se nao tiver coloca como string
        if column_type != "":
            if column_type in cast_types:
                column_type = cast_types[column_type]
            else:
                column_type = cast_types['string']

            create_external_table += "\t" + column_name + " " + column_type

            if index != len(columns) - 1:
                create_external_table += ","

            create_external_table += "\n"

        index += 1;

    create_external_table += ") \n"

    create_external_table += " \
        WITH (  \n \
        \t LOCATION = 'project/{}',  \n \
        \t DATA_SOURCE = [gold], \n \
        \t FILE_FORMAT = [DeltaFormat] \n \
    ) \n ".format(table_raw_name)

    # LOCATION = path da tabela no container
    # DATA_SOURCE = container utilizado no storage
    # FILE_FORMAT = tipo de arquivo da tabela externa
    create_external_table += "GO \n"

    
print(create_external_table)   #gera o script sql de criação da external table 

# COMMAND ----------

#script de drop das tabelas externas no synapse
spark.sql('use {}'.format(database_raw_name))

drop_external_table = ""

for row in spark.sql('show tables').collect():
    drop_external_table += """
        IF OBJECT_ID('dbo.{}') IS NOT NULL
        BEGIN
            DROP EXTERNAL TABLE [dbo].[{}]
        END \n
    """.format(row['tableName'], row['tableName'])
    drop_external_table += "GO \n"
  
print(drop_external_table)