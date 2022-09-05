import json
import requests

id_deudor = int(input('Introduzaca el Id_deudor: '))
url = "https://w1vh5d7mu5.execute-api.us-east-2.amazonaws.com/facturedo-post"
dict_id_deudor = json.dumps({'id_deudor':id_deudor})
response = requests.post(url,dict_id_deudor)
print(json.loads(response.text))