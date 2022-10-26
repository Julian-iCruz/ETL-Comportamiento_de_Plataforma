# Tabla de contenido

[[_TOC_]]

# 1. Ejecucion Main
Para la ejecución del archivo **main.py** se recomienda crear un entorno de conda con la versión de **Python 3.10.4**, las librerías que son necesaria para su ejecución son:

- numpy==1.23.2
- openpyxl==3.0.10
- pandas==1.4.4

Ejecutando el comando:
```bash
python3 main.py
```

Se ejecutará el programa el cual contiene la lógica de los cálculos pedidos, este programa no tiene la conexión hacia la API. Se debe introducir el **id_deudor** del cual se desean conocer las métricas.

La salida de esta ejecución da como resultado un archivo **dataset.csv** que es el que debe ser insertado en el [bucket S3](https://s3.console.aws.amazon.com/s3/buckets/facturedo-raw?region=us-east-2&prefix=data-engineer/&showversions=false) para desencadenar la ejecución del proceso ETL en AWS, de igual manera devuelve un diccionario con cada uno de los cálculos requeridos.

# 2. Ejecucion API REST

Para la ejecucion del archivo **Api_Rest_facturedo.py** se recomienda crear un entorno de conda con la version de **Python 3.10.4**, las librerias que son necesaria para su ejecucion son:

- numpy==1.23.2
- openpyxl==3.0.10
- pandas==1.4.4
- requests==2.28.1

Ejecutando el comando:
```bash
python3 Api_Rest_facturedo.py
```

Se ejecuta el programa que realiza una peticion al API REST creada en AWS que retornara en forma de diccionario cada uno de los calulos y metricas para el deudor que se envie por consola.
