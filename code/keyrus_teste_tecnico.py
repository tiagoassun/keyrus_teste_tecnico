# -*- coding: utf-8 -*-
"""keyrus-teste-tecnico.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iBnnlAClXzsmKvoeLDMeVwX8AY-DgW7r

# Teste Técnico keyrus - Engenharia de Dados - Case 2

## 1 - Baixando, instalando e configurando o Apache Spark
"""

# Instalar as dependências
!apt-get install openjdk-8-jdk-headless -qq > /dev/null

# Baixando Apche Spark que será salvo em no diretorio "/content/"
!wget -q https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
!tar xf spark-3.2.0-bin-hadoop3.2.tgz

# Baixando bibliotecas
!pip install -q findspark
!pip install pyspark[sql]
!pip install seaborn
!pip install geopandas

# Configurar as variáveis de ambiente do Linux que o Google Colab roda em cima
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.2.0-bin-hadoop3.2"

# Tornar o pyspark "importável"
import findspark
findspark.init('spark-3.2.0-bin-hadoop3.2')

# Iniciar uma sessão local
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext

spark = SparkSession.builder.master('local[*]').getOrCreate()

# Import de tipos do Spark
from pyspark.sql.functions import *
from pyspark.sql.window import Window

"""## 2 - Transformações dos dados

### 2.1 - Importando e lendo .CSV
"""

# Download do CSV para local, que será salvo no diretorio "/content/"
!wget --quiet --show-progress https://raw.githubusercontent.com/tiagoassun/keyrus_teste_tecnico/main/file/cadastro-individual-MUNICIPIO-fim.csv

# Carregar dados dos municípios
df_municipio_csv = spark.read \
                .format("csv") \
                .option("header", "true") \
                .option("encoding", "ISO-8859-1") \
                .load("./cadastro-individual-MUNICIPIO-fim.csv")

df_municipio_csv.printSchema()

"""### 2.2 - Modificando schema do DF"""

# Convertando colunas para valores inteiros
# Renomeando colunas
# Retirando colunas
df_municipio_cast = df_municipio_csv \
                        .withColumn('transacao', col("valor").cast('int')) \
                        .withColumnRenamed("uf", "estado") \
                        .withColumnRenamed("ano", "data_atualizacao") \
                        .drop('ibge', 'parametro', 'ano_quadrimestre', 'quadrimestre', 'valor')

df_municipio_cast.printSchema()

df_municipio_cast.show(10, False)

"""### 2.3 - Agrupando dados"""

df_municipio_agrupado = df_municipio_cast \
            .groupBy("estado", "municipio", "data_atualizacao")\
            .agg(sum('transacao').alias("transacao_por_ano")) \
            .orderBy("data_atualizacao")

df_municipio_agrupado.where("municipio = 'VITÓRIA'").show(10, False)

"""### 2.4 - Criando ordem da transação

#### 2.4.1 - Em SQL
"""

# Criando tabela temporaria no Spark para poder usar consulta SQL
df_municipio_agrupado.select('estado', 'municipio', 'data_atualizacao', 'transacao_por_ano').createOrReplaceTempView('tb_df_municipio_agrupado_temp')

query_sql = """
SELECT 
    tb_temp.*, 
    RANK() OVER (PARTITION BY municipio ORDER BY municipio, data_atualizacao) AS ordem_transacao
FROM tb_df_municipio_agrupado_temp AS tb_temp
"""

df_municipio_final_sql = spark.sql(query_sql)

# Dropando a tabela temporaria pois não precisamos mais dela
spark.catalog.dropTempView("tb_df_municipio_agrupado_temp")

df_municipio_final_sql.show(10, False)

"""##### 2.4.1.1 - Gravando dados"""

#Salvandos os dados localmente em "/content/municipio_final_sql"
PATH = "./municipio_final_sql"

df_municipio_final_sql.coalesce(1) \
        .write \
        .mode("overwrite") \
        .save(PATH, format="parquet")

"""#### 2.4.2 - Em PySpark"""

janela = Window().partitionBy("municipio").orderBy("municipio", "data_atualizacao")

df_municipio_final_pyspark = df_municipio_agrupado \
                                    .withColumn("ordem_transacao", rank().over(janela))

df_municipio_final_pyspark.show(10, False)

"""##### 2.4.2.1 - Gravando dados"""

#Salvandos os dados localmente em "/content/municipio_final_pyspark"

PATH = "./municipio_final_pyspark"

df_municipio_final_pyspark.coalesce(1) \
    .write \
    .mode("overwrite") \
    .save(PATH, format="orc")