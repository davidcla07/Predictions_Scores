import json
import time
import requests
import pandas as pd
from pandas import ExcelWriter
import openpyxl
from openpyxl import load_workbook
from itertools import chain
from collections import defaultdict
import csv

#explorar y recuperar datos
dict3 = defaultdict(list)

# Use the file name partidos.txt as the file name
fname = input("Enter file:")
if len(fname) < 1 :
    name = "partidos.txt"
    fh=open(name)
for line in fh : #este ciclo busca cada frase del texto
    if len(line) < 1 : #guardian, evita error en busqueda sin texto
        continue
    else:
        partido=line.strip() #id del partido para buscar en API los datos del partido

        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"
        querystring={"fixture":partido}
        apikey="ingresar api key"

        headers = {'x-rapidapi-key': apikey,'x-rapidapi-host': "api-football-v1.p.rapidapi.com"}
        response = requests.request("GET", url, headers=headers,params=querystring)

        if response.status_code==200:
            content=response.content
            datos=json.loads(content)
            respuesta=datos["response"]
    #se extraen todos los parametros de los datos recibidos

            name_local=respuesta[0]["team"]["name"]
            shotsongoal_local=respuesta[0]["statistics"][0]["value"]
            totalshots_local=respuesta[0]["statistics"][2]["value"]
            fouls_local=respuesta[0]["statistics"][6]["value"]
            corners_local=respuesta[0]["statistics"][7]["value"]
            posesion_local=respuesta[0]["statistics"][9]["value"]
            posesion_local=int(posesion_local[:2])
            TA_local=respuesta[0]["statistics"][10]["value"]
            TR_local=respuesta[0]["statistics"][11]["value"]

            name_visitante=respuesta[1]["team"]["name"]
            shotsongoal_visita=respuesta[1]["statistics"][0]["value"]
            totalshots_visita=respuesta[1]["statistics"][2]["value"]
            fouls_visita=respuesta[1]["statistics"][6]["value"]
            corners_visita=respuesta[1]["statistics"][7]["value"]
            posesion_visita=respuesta[1]["statistics"][9]["value"]
            posesion_visita=int(posesion_visita[:2])
            TA_visita=respuesta[1]["statistics"][10]["value"]
            TR_visita=respuesta[1]["statistics"][11]["value"]

            id_partido=int(partido)
    #se crea el diccionario de la matriz de datos como se requieren
            dict_datos={"id partido":id_partido,"local":name_local,"visitante":name_visitante,
                        "Tiros Total L":totalshots_local,"Tiros Total V":totalshots_visita,
                        "Tiros Arco L":shotsongoal_local,"Tiros Arco V":shotsongoal_visita,
                        "Posesion L":posesion_local,"Posesion V":posesion_visita,
                        "Fouls L":fouls_local,"Fouls V":fouls_visita,
                        "TA L":TA_local,"TA V":TA_visita,
                        "TR L":TR_local,"TR V":TR_visita,
                        "Corners L":corners_local,"Corners V":corners_visita}

    #almacenar las estadisticas por cada partido
            dict1 = dict_datos
            for k, v in chain(dict1.items()):
                dict3[k].append(v)
        elif response.status_code==204:
            print(partido,":No content")
        elif response.status_code==499:
            print(partido,":Time Out")
        elif response.status_code==500:
            print(partido,":Error server")
    time.sleep(10)

#convertir el diccionario con todos los datos en un DataFrame
df=pd.DataFrame(dict3)

df=df[["id partido","local","visitante",
       "Tiros Total L","Tiros Total V","Tiros Arco L","Tiros Arco V",
       "Posesion L","Posesion V","Fouls L","Fouls V",
       "TA L","TA V","TR L","TR V","Corners L","Corners V"]] #ordenar los datos en el DataFrame

#archivo base de datos
file_results="C:/Users/MSI/Desktop/ejercicios/API futbol/estd_partidos.xlsx"
#encontrar el numero de filas con datos
data_excel=pd.read_excel(file_results,"Sheet1")
fila_inicio=data_excel.shape[0]

#convertir el Dataframe a excel
book = load_workbook("C:/Users/MSI/Desktop/ejercicios/API futbol/estd_partidos.xlsx")
writer = pd.ExcelWriter("C:/Users/MSI/Desktop/ejercicios/API futbol/estd_partidos.xlsx", engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
df.to_excel(writer, book.worksheets[0].title, startrow = fila_inicio+1,  index = False,header=False)
writer.save()

print("Writing complete")
