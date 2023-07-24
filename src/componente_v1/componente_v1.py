import os
import subprocess
import requests
import json
import logging


class Comando:
    def __init__(self, script_path, args):
        self.script_path = script_path
        self.args = args

    def ejecutar(self):
        try:
            response = subprocess.run(
                ["python3", self.script_path] + self.args,
                capture_output=True,
                text=True,
                check=True
            )
            # resultado = json.loads(response.stdout)
            return self._procesar_salida(response)
        except Exception as e:
            logging.error(f"Error al ejecutar el script: {e}")
            raise
    
    def _procesar_salida(self, response):
        try:
            resultado = json.loads(response.stdout)
            return resultado
        except json.JSONDecodeError:
                logging.warning("La salida del script no es JSON válido.")
                return str(response.stdout)


class Componente:
    def __init__(self, comando, url, timeout=20):
        self.comando = comando
        self.url = url
        self.timeout = timeout


    def gestionar(self):
        try:
            resultado = self.comando.ejecutar()
            return self._enviar_a_access_manager(resultado)
        except Exception as e:
            logging.error(f"Error en la gestión: {e}")
            raise

    def _enviar_a_access_manager(self, resultado):
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(self.url, headers=headers, data=json.dumps(resultado), timeout=self.timeout)
            return response.status_code
        except requests.exceptions.RequestException as e:
            logging.error(f"Error al enviar los datos al Access Manager: {e}")
            raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    script_path = os.getenv('SCRIPT_PATH')
    args = os.getenv('ARGS').split()  # asumimos que los argumentos están separados por espacios
    url = os.getenv('URL')

    comando = Comando(script_path, args)
    componente = Componente(comando, url)

    try:
        resultado = componente.gestionar()
        logging.info(f"Resultado: {resultado}")
    except Exception as e:
        logging.error(f"Error en el programa principal: {e}")

