import requests
import json
import pandas as pd
from openpyxl import load_workbook
from itertools import chain
from collections import defaultdict

print("id por torneo:")
print("La Liga:140")
print("Premier League:39")
print("Bundesliga:78")
print("Serie A:135")
print("Eredivisie:88")
print("Ligue 1:61")
id_league=input("Ingrese id del torneo:")
round=input("Ingrese No Jornada:")
round="Regular Season - "+round
url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
apikey="ingresar api key"
querystring = {"league":id_league,"season":"2020","round":round}

headers = {
    'x-rapidapi-key': apikey,
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
content=response.content
datos=json.loads(content)
respuesta=datos["response"]
dict3 = defaultdict(list)
cont=0
for i in respuesta:
#navegar en el archivo Json
    info=respuesta[cont]
    id_partido=info["fixture"]["id"]
    arbitro=info["fixture"]["referee"]
    jornada=info["league"]["round"]
    gol_local=info["goals"]["home"]
    gol_visita=info["goals"]["away"]
    liga=info["league"]["name"]
    local=info["teams"]["home"]["name"]
    visitante=info["teams"]["away"]["name"]
#crear diccionario con las estadisticas
    dict_datos={"id_partido":id_partido,"Fecha":jornada,"goles L":gol_local,"goles V":gol_visita,
                 "Arbitro":arbitro,"Local":local,"Visitante":visitante,"Torneo":liga}
    #almacenar las estadisticas por cada partido
    dict1 = dict_datos
    for k, v in chain(dict1.items()):
        dict3[k].append(v)
    cont+=1
#convertir el diccionario con todos los datos en un DataFrame
df=pd.DataFrame(dict3)

df=df[["Torneo","Fecha","id_partido","Local","Visitante","goles L","goles V","Arbitro"]] #ordenar los datos en el DataFrame

#archivo base de datos
file_results="C:/Users/david/Desktop/ejercicios/API futbol/datos_fechas.xlsx"
#encontrar el numero de filas con datos
data_excel=pd.read_excel(file_results,"Sheet1")
fila_inicio=data_excel.shape[0]

#convertir el Dataframe a excel
book = load_workbook("C:/Users/david/Desktop/ejercicios/API futbol/datos_fechas.xlsx")
writer = pd.ExcelWriter("C:/Users/david/Desktop/ejercicios/API futbol/datos_fechas.xlsx", engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
df.to_excel(writer, book.worksheets[0].title, startrow = fila_inicio+1,  index = False,header=False)
writer.save()

print("Writing complete")
