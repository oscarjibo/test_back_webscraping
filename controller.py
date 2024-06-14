
import pandas as pd
from extract_data import filter_data, extract_detail, extract_data, extract_actions, data_organice 
import uuid
from datetime import datetime
import os

"""
controlador de procesos, en esta parte el proceso llama una a una las funciones encargadas de extraer data 
1. llamar y extraer la data
2. contiene los logs para obtener el estado de las peticiones 
3. guarda y almacena la tabla de salida como un archivo xlsx el cual contieen identificador unico, variables y un JSON con toda la data
que se requiere en el proceso
4. regresa una tabla tipo dataframe la cual renderiza el HTML
"""
save_path = "C:/Users/FJ669RR/OneDrive - EY/Desktop/Prueba/Volumes/Output" #ruta para guardar la data de salida

def web_scrapping_process(id:str):
    try:
        response =  {"data": {}, "status": "", "detail": ""}
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{date} ====== iniciando el proceso de extracción de data para el usuario con ID: {id} ...")
        print(f"{date} ====== Extrayendo data...")
        initial_data = extract_data(id)
        print(f"{date} ====== Filtrando data...")
        filter_data_web = filter_data(initial_data[0], initial_data[1])
        print(f"{date} ====== Extrayendo details...")
        add_details_demandante = extract_detail(filter_data_web[0]) 
        add_details_demandado  = extract_detail(filter_data_web[1])
        print(f"{date} ====== Extrayendo acciones...")
        add_actions_demandante = extract_actions(add_details_demandante)
        add_actions_demandado  = extract_actions(add_details_demandado)
        data_insert = []
        data = add_actions_demandado + add_actions_demandante
        print(f"{date} ====== Creando estructura...")
        if not data:
            detail = "NO EXISTE DATA PARA ESE USUARIO"
            final_data = pd.DataFrame()
            file_path = ""
        else:
            for value in data:
                payload = {"uuid_consulta": str(uuid.uuid4()),
                           "personal_id": value['personal_id'],
                           "id_juicio": value['idJuicio'],
                           "tipo": value['type'],
                           "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                           "data_consulta": value
                }
                data_insert.append(payload)
            final_data = pd.DataFrame(data_insert)
            print(final_data,"final data")
            date = datetime.now().strftime("%Y_%m_%d")
            file_name = f"{date}_Consulta_web_scrapping_{id}_procesos_judiciales.xlsx"
            file_path = os.path.join(save_path, file_name)
            final_data.to_excel(file_path)
            print(f"{date} ===== Finalizado correctamente ...")
            print(final_data)
            final_data = data_organice(final_data)
            detail = "Usuario consultado correctamente."
        return (final_data, detail, file_path)
    except Exception as e:
        print("ERROR WEB SCRAPING")
        e = f"Error found in process: error: {e}"
        return e

