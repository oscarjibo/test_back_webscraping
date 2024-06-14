import threading
import unittest
from main import web_scrapping_process
from extract_data import clean_html, extract_actions, extract_data, extract_detail, filter_data
from test_data import *


"""
dentro de este modulo esta:

1. deploy_parallel: funcion que nos genera 15 pruebas de manera paralela con el fin de intentar bloquear las solicitudes:

conclusion: el ancho de banda permite que las peticiones se generen

2. clase: Unittest:

permite realizar pruebas unitarias a cada funcion corroborando la salida de cada funcion y el tipo de variable que retorna


"""
 # ejecuto las 15 en paralelo
def deploy_parallel(function, args):
  threads = []
  for indice in range(15):
    thread = threading.Thread(target=deploy_script, args=(indice, function, args))
    threads.append(thread)
    thread.start()
  for thread in threads:
    thread.join()

# funcion que me ejecuta mi prueba
def deploy_script(indice, function, args):
  try:
    print(f"Iniciando prueba {indice} con argumento {args}")
    web_scrapping_process(args)
    print(f"Finalizando prueba {indice}")
  except Exception as e:
    print("ERROR",e)

id = "0968599020001"
web_scrapping_process(id)
deploy_parallel(web_scrapping_process, id)


####### TEST UNITARIOS ####################

class TestExtractData(unittest.TestCase):
    def test_extract_data(self):
        resultado = clean_html(payload_clean_html)
        self.assertIsInstance(resultado, str)  # Verifica que el resultado sea una lista

class TestExtractData(unittest.TestCase):
    def test_extract_data(self):
        resultado = extract_data(payload_extract_data)
        self.assertIsInstance(resultado, tuple)  # Verifica que el resultado sea una lista
        self.assertEqual(resultado, payload_extract_data_output)  # Verifica que el contenido sea el esperado

class TestFilterData(unittest.TestCase):
    def test_filter_data(self):
        resultado = filter_data(payload_extract_data_output[0], payload_extract_data_output[1])
        self.assertIsInstance(resultado, tuple)  # Verifica que el resultado sea una lista

class ExtractDetails(unittest.TestCase):
    def test_extract_detail(self):
        resultado = extract_detail(payload_extract_detail[0])
        self.assertIsInstance(resultado, list)  # Verifica que el resultado sea una lista

class ExtractActions(unittest.TestCase):
    def test_extract_actions(self):
        resultado = extract_detail(payload_extract_actions)
        self.assertIsInstance(resultado, list)  # Verifica que el resultado sea una lista


if __name__ == '__main__':
    unittest.main()





















def test_extract_data(payload):
  response = {  "status": ""
              , "detail": ""
              , "data": {}
             }
  try:
    data = extract_data(payload_extract_data)
    response["data"] = data
    response['detail'] = "Complete"
    response["status"] = "200"
  except Exception as e:
    e = f"error in extract data process,  error : {e}"
    response["data"] = []
    response['detail'] = e 
    response["status"] = "400"
  return response




#test extract data

#test filter data

#test extract data detail

#test extract actions







