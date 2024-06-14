import requests
import pandas as pd
import json
from bs4 import BeautifulSoup


"""
funciones para extraer la data 

1.clean_html: la peticion arroja como action un str en formato html, esta funcion se encarga de limpiarlo y dejarlo como un str

2.extract_data: realiza una peticion post mediante un payload que se configura con el id que el usuario ingresa

3.filter_data: realiza el filtrado de la data asi como la agregación de llaves para distinguir demandante y demandado 

4.extract_details: realiza peticiones get para obtener los details de cada uno de los procesos

5.extract_actions: realiza peticiones post las cuales obtiene las acciones de cada uno de los detalles 

6.organice_data: organiza la data de la forma que queremos mostrarla en el html

"""
def clean_html(raw_html):
    try:
        if str == '':
            return ''
        else:
            soup = BeautifulSoup(raw_html, "html.parser")
            return soup.get_text()
    except Exception as e:
        return f"error in clean html: {e}"
    
def extract_data(id:str):
    try:
        url = "https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/buscarCausas?page=1&size=1000"
        payload_actor = {"page": 1,"size": 10,"numeroCausa": "","actor": {"cedulaActor": id, "nombreActor": ""},"demandado": {"cedulaDemandado": "", "nombreDemandado": ""},"first": 1,"numeroFiscalia": "","pageSize": 10,"provincia": "","recaptcha": "verdad"}
        payload_demandado = {"page": 1,"size": 10,"numeroCausa": "","actor": {"cedulaActor": "", "nombreActor": ""},"demandado": {"cedulaDemandado": id, "nombreDemandado": ""},"first": 1,"numeroFiscalia": "","pageSize": 10,"provincia": "","recaptcha": "verdad"}
        headers = { "Content-Type": "application/json"}
        response_actor = requests.post(url, json=payload_actor, headers=headers)
        response_demandado = requests.post(url, json=payload_demandado, headers=headers)
        if response_actor.status_code == 200:
            data_actor = response_actor.content
            data_actor = data_actor.decode("utf-8")
            data_actor = json.loads(data_actor)
            for value in data_actor:
                value['personal_id'] = id
        else:
            data_actor = []
        if response_demandado.status_code == 200:
            data_demandado = response_demandado.content
            data_demandado = data_demandado.decode("utf-8")
            data_demandado = json.loads(data_demandado)
            for value in data_demandado:
                value['personal_id'] = id
        else:
            data_demandado = []
        return (data_actor, data_demandado)
    except Exception as e:
        return f"error in extract data: {e}"
    

def filter_data(data_actor:list, data_demandado:list):
    try:
        data_insert_actor = []
        data_insert_demandado = []
        if not data_actor:
            data_insert_actor = []
        else:
            for value_actor in data_actor:
                value_actor['type'] = 'Demandante'
                value_actor['details'] = []
                data_insert_actor.append(value_actor)
        if not data_demandado:
            data_insert_demandado = []
        else:
            for value_demandado in data_demandado:
                value_demandado['type'] = 'Demandado'
                value_demandado['details'] = []
                data_insert_demandado.append(value_demandado)
        return (data_insert_actor, data_insert_demandado)
    except Exception as e:
        return f"error in filter data: {e}"

def extract_detail(data:list):
    try:
        if not data:
            data = []
        else:
            for process in data:
                process_numer = process['idJuicio']
                url_detail = f"https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/consulta-causas-clex/informacion/getIncidenteJudicatura/{process_numer}"
                detail = requests.get(url_detail)
                if detail.status_code == 200:
                    detail = detail.content
                    detail = detail.decode("utf-8")
                    detail = json.loads(detail)
                    process['details'] = detail
                else:
                    process['details'] = {}
        return data
    except Exception as e:
        return f"error in extract detail: {e}"

def extract_actions(data:list):
    try:
        if not data:
            data = []
        else:
            url_extract_actions = "https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/actuacionesJudiciales"
            headers = {"Content-Type": "application/json"}
            for value in data:
                payload_actions = {
                            "idMovimientoJuicioIncidente": value['details'][0]['lstIncidenteJudicatura'][0]['idMovimientoJuicioIncidente'],
                            "idJuicio": value['idJuicio'],
                            "idJudicatura": value['details'][0]['lstIncidenteJudicatura'][0]['idJudicaturaDestino'],
                            "aplicativo": "web",
                            "idIncidenteJudicatura": value['details'][0]['lstIncidenteJudicatura'][0]['idIncidenteJudicatura'],
                            "incidente": value['details'][0]['lstIncidenteJudicatura'][0]['incidente'],
                            "nombreJudicatura": value['details'][0]['nombreJudicatura']
                            }
                response = requests.post(url_extract_actions, json=payload_actions, headers=headers)
                if response.status_code == 200:
                    data_actions = response.json()
                    for action in data_actions:
                        action['actividad'] = str(clean_html(action['actividad']))
                        action['actividad'] = action['actividad'].replace('"','')  
                        action['actividad'] = action['actividad'].replace(':','') 
                        action['actividad'] = action['actividad'].replace(',','') 
                    value['details'][0]['actions'] = data_actions
                else:
                    data_actions = []
        return data
    except Exception as e:
        return f"error in extract actions: {e}"

def data_organice(data):
    if len(data) == 0:
        final_data_view = []
    else:
        data_view_html = []
        for value in range(len(data)):
            data_enter = data.iloc[value]
            data_filter = data_enter['data_consulta']
            data_view = {"id juicio": data_filter['idJuicio'],
                         "tipo": data_enter['tipo'],
                         "details": data_filter['details'],
                         "actions": data_filter['details'][0]['actions']}
            data_view_html.append(data_view)
        final_data_view = pd.DataFrame(data_view_html)
    return final_data_view




