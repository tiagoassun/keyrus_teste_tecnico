# Teste Técnico de Engenharia de Dados

> **Para abrir o código diretamente no Google Colab por favor [clique aqui.](https://colab.research.google.com/drive/1iBnnlAClXzsmKvoeLDMeVwX8AY-DgW7r?usp=sharing)**

## 1 - Google Colaboratory (Google Colab)
Todo o teste foi feito utilizando o ambiente Google Colab. 

O Google Colab é um ambiente de notebooks Jupyter que não requer configuração e é executado na nuvem. 

Nele é possível escrever e executar códigos em Python, salvar e compartilhar suas análises além de acesso a poderosos recursos de computação científica, tudo disponibilizado pela Google gratuitamente no seu navegador.

Como se trata no final das contas de um Jupyter Notebook, é possével utilizar os comando do Jupyter Notebook.

* Os comandos de bash podem ser executados prefixando o comando com ```“!”```.

```bash
!git clone https://github.com/tiagoassun/keyrus_teste_tecnico.git
```

~~~bash
!ls -la
~~~

~~~bash
!wget -q https://archive.apache.org/dist/spark/spark-3.2.0/spark-3.2.0-bin-hadoop3.2.tgz
~~~

~~~bash
!tar xf spark-2.4.4-bin-hadoop2.7.tgz
~~~

~~~bash
!pip install -q findspark
~~~

~~~bash
!apt-get install openjdk-8-jdk-headless -qq > /dev/null
~~~


> **Para abrir o código diretamente no Google Colab por favor [clique aqui.](https://colab.research.google.com/drive/1iBnnlAClXzsmKvoeLDMeVwX8AY-DgW7r?usp=sharing)**



## 2 - Visualizando arquivos salvos localmente

Para salvar os DFs em formato “parquet” e “orc”, usamos os dois códigos abaixo:

~~~python
PATH = "./municipio_final_sql"

df_municipio_final_sql.coalesce(1) \
        .write \
        .mode("overwrite") \
        .save(PATH, format="parquet")
~~~

~~~python
PATH = "./municipio_final_pyspark"

df_municipio_final_pyspark.coalesce(1) \
    .write \
    .mode("overwrite") \
    .save(PATH, format="orc")
~~~

> Para visualizar os arquivos que foram salvos localmente, é só clicar no ícone de "arquivos" que o Google Colab por padrão irá te colocar em "/content", e com isso é possível visualizar os arquivos salvos.
![1](https://raw.githubusercontent.com/tiagoassun/keyrus_teste_tecnico/main/images-readme/1.png)



> **Para abrir o código diretamente no Google Colab por favor [clique aqui.](hhttps://colab.research.google.com/drive/1iBnnlAClXzsmKvoeLDMeVwX8AY-DgW7r?usp=sharing)**
