import pytest
import requests
import requests_mock
from unittest.mock import Mock, patch
from src.componente_v1.componente_v1 import Comando




@patch('subprocess.run')
def test_ejecutar(mocked_run):
    # Define la salida de subprocess.run
    mock_response = Mock()
    mock_response.stdout = '{"resultado": "ok"}'
    mocked_run.return_value = mock_response

    comando = Comando("script.py", ["arg1", "arg2"])
    resultado = comando.ejecutar()

    assert resultado == {"resultado": "ok"}

def test_fixture(requests_mock):
    requests_mock.get("http://123-fake-api.com", text="Hello!")

    response = requests.get("http://123-fake-api.com")

    assert response.text == "Hello!"


# TESTS UNITARIOS Comando.ejecutar()
# Prueba que un resultado exitoso de la ejecución del script se procesa correctamente.
mocked_response = Mock()
mocked_response.stdout = '{"resultado": "ok"}'
@patch('subprocess.run', return_value=mocked_response)
def test_comando_ejecutar_exitoso(mocked_run):
    comando = Comando("script.py", ["arg1", "arg2"])
    resultado = comando.ejecutar()
    assert resultado == {"resultado": "ok"}
# Prueba que un error en la ejecución del script se maneja correctamente.
@patch('subprocess.run', side_effect=Exception('Error al ejecutar el script'))
def test_comando_ejecutar_error(mocked_run):
    comando = Comando("script.py", ["arg1", "arg2"])
    resultado = comando.ejecutar()
    assert resultado == 'Error al ejecutar el script'
# Prueba que la salida no JSON del script se maneja correctamente.
mocked_response_no_json = Mock()
mocked_response_no_json.stdout = 'resultado: ok'
@patch('subprocess.run', return_value=mocked_response_no_json)
def test_comando_ejecutar_no_json(mocked_run):
    comando = Comando("script.py", ["arg1", "arg2"])
    resultado = comando.ejecutar()
    assert resultado == 'resultado: ok'

# TESTS UNITARIOS Componente.enviar_a_access_manager()
# Prueba que los resultados se envían correctamente al Access Manager.
# Prueba que se maneja correctamente una respuesta exitosa del Access Manager.
# Prueba que se maneja correctamente una respuesta de error del Access Manager.
# Prueba que se maneja correctamente un timeout del Access Manager.

# TESTS UNITARIOS Componente.gestionar()
# Prueba que una ejecución y envío exitosos de los resultados se manejan correctamente.
# Prueba que un error en la ejecución del script se maneja correctamente.
# Prueba que un error en el envío de los resultados al Access Manager se maneja correctamente.

# TESTS DE INTEGRACIÓN
# Prueba el flujo completo de ejecutar el script y enviar los resultados al Access Manager.
# Prueba el manejo de errores en todo el flujo.

# PRUEBAS DE TOLERANCIA A FALLOS
# Prueba que si el script falla, el error se maneja correctamente y no hace fallar todo el Componente.
# Prueba que si el Access Manager no está disponible o tarda demasiado en responder, el error se maneja correctamente y no hace fallar todo el Componente.



# Ahora ejecutamos las pruebas
test_comando_ejecutar_exitoso()
test_comando_ejecutar_no_json()
test_comando_ejecutar_error()











