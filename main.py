import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta 

def convertColumnsToDate(df, column_List_Convert):
    for i in column_List_Convert:
        df[i] = convertStringToDate(df[i])
    return df

def convertStringToDate(df):
        return pd.to_datetime(df, format='%Y-%m-%d')
    
def convertDfToDictionary(df):
    columns = df.columns.to_list()
    return dict([(x, y) for x, y in zip(df[columns[0]], df[columns[1]])])

def countResults(df):
    df_Result_Count = df['result'].value_counts().reset_index()
    return convertDfToDictionary(df_Result_Count)

def averagePaymentDays(df):
    df_Days = pd.DataFrame()
    df_Days['days'] =  (df['payment_date']  - df['creation_date']).dt.days
    df_Payment_Days = pd.concat([df[['creation_date','payment_date']], df_Days], axis=1)
    return round(df_Payment_Days['days'].mean())

def calculateIqrLimits(df):
    q3, q1 = np.percentile(df['amount'], [75, 25])
    iqr = q3 - q1
    umbral_superior = q3 + 1.5 * iqr
    umbral_inferior = q1 - 1.5 * iqr
    return {'umbral_superior':umbral_superior,'umbral_inferior':umbral_inferior}

def calculateMaxVolumeByPayMethod(df):
    df_Volumen_PayMethod = df[['anual_sales_volume','payment_method']]
    df_Groupby = df_Volumen_PayMethod.groupby('payment_method')['anual_sales_volume'].agg(Max_Volume = 'max').reset_index()
    df_Groupby['payment_method'] = df_Groupby['payment_method'].replace({"'":""}, regex=True)
    return convertDfToDictionary(df_Groupby)

def extractUpperThresholdOperations(df, upper_Threshold):
    df_Upper_Threshold_Operations = df[df['amount']>upper_Threshold]
    df__Operations_Id = df_Upper_Threshold_Operations[['operation_id','amount']]
    return convertDfToDictionary(df__Operations_Id)

def calulateAbgMaxlastMonths(df, months, current_Date):
    df_Creation_Date_Amount = df[['amount','creation_date']] 
    last_date = current_Date - relativedelta(months = months)
    df_Date_Filtered = df_Creation_Date_Amount[(df_Creation_Date_Amount['creation_date'] <= current_Date) & (df_Creation_Date_Amount['creation_date'] > last_date)]
    df_Months_Years = pd.DataFrame()
    df_Months_Years['Year'] = df_Date_Filtered['creation_date'].dt.year 
    df_Months_Years['Month'] = df_Date_Filtered['creation_date'].dt.month 
    df_Date_Filtered = pd.concat([df_Date_Filtered, df_Months_Years], axis=1)
    df_Groupby_Month_Year = df_Date_Filtered.groupby(['Year', 'Month'])['amount'].agg(Max_Amount = 'max').reset_index()
    return round(df_Groupby_Month_Year['Max_Amount'].mean())

def extractNullField(df):
    df_Date_Index = df.set_index('Fecha carga DL') 
    list_Row_Column = [] 
    df_Columns_True_False = df_Date_Index.isnull()
    list_Columns = df_Columns_True_False.any()
    list_Null_Columns = list(list_Columns[list_Columns == True].index) 

    for col in list_Null_Columns: 
        rows = list(df_Columns_True_False[col][df_Columns_True_False[col] == True].index) 
        for row in rows: 
            list_Row_Column.append((str(row).split(' ')[0], col))

    return dict(list_Row_Column)

if __name__ == "__main__":
    id_deudor = int(input('Introduzaca el id_deudor: '))
    data = pd.read_excel('Dataset_v3.xlsx')
    data.to_csv('dataset.csv', index=False)
    df = pd.read_csv('dataset.csv')
    df = convertColumnsToDate(df,['Fecha carga DL','creation_date','payment_date'])
    df_By_Deudor = df[df['id deudor'] == id_deudor]
    if len(df_By_Deudor)!=0:
        output = {id_deudor :{
            'conteo_operaciones': countResults(df_By_Deudor),
            'dias_promedio_pago_ops_pagadas': averagePaymentDays(df_By_Deudor),
            'umbrales_outliers': calculateIqrLimits(df_By_Deudor),
            'tipo_pago_max_volumen': calculateMaxVolumeByPayMethod(df_By_Deudor),
            'lista_operaciones': extractUpperThresholdOperations(df_By_Deudor, 15000),
            'prom_max_ult_6_meses': calulateAbgMaxlastMonths(df_By_Deudor, 6, datetime.strptime('2022-08-24', '%Y-%m-%d')),
            'valores_nulos': extractNullField(df_By_Deudor)
            }
        }
        print(output[id_deudor])
    else:
        print({'body':'Deudor no existe'})