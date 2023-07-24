import os
import subprocess
import requests
import json

class Comando:
    def __init__(self, script_path, args):
        self.script_path = script_path
        self.args = args

    def ejecutar(self):
        response = subprocess.run(
            ["python3", self.script_path] + self.args,
            capture_output=True,
            text=True,
            check=True
        )
        resultado = json.loads(response.stdout)
        try:
            resultado = json.loads(response.stdout)
        except json.JSONDecodeError:
            resultado = str(response.stdout)
        print(f"Resutlado: {resultado}")
        return resultado

class Componente:
    def __init__(self, comando, url):
        self.comando = comando
        self.url = url

    def gestionar(self):
        resultado = self.comando.ejecutar()
        return self.enviar_a_access_manager(resultado)

    def enviar_a_access_manager(self, resultado):
        print(f"URL: {self.url}")
        print(f'RESULTADO {resultado}')

        headers = {"Content-Type": "application/json"}
        response = requests.post( 'http://host.docker.internal:8080/results', headers=headers, data=json.dumps(resultado), timeout=20)
        print("Response from server:", response.text)
        return 10

    

if __name__ == "__main__":
    script_path = os.getenv('SCRIPT_PATH')
    args = os.getenv('ARGS').split()  # asumimos que los argumentos están separados por espacios
    url = os.getenv('URL')
    comando = Comando(script_path, args)
    componente = Componente(comando, url)
    resultado = componente.gestionar()
    print(f"Resultado: {resultado}")


"""En este código, hemos dividido las responsabilidades entre dos clases: Comando y Componente.

La clase Comando encapsula el script de Python que quieres ejecutar, junto con cualquier argumento necesario. Cuando se ejecuta el método ejecutar de Comando, se ejecuta el script y se recoge su salida.

Por otro lado, la clase Componente es responsable de gestionar el proceso. Toma un objeto Comando y una URL como argumentos de su constructor. Cuando se ejecuta el método gestionar de Componente, ejecuta el comando, recoge su salida y la envía a la URL proporcionada.

Este diseño tiene la ventaja de ser muy flexible. Puedes crear diferentes comandos y pasarlos a un Componente para su ejecución. De esta manera, puedes cambiar fácilmente lo que hace Componente simplemente pasándole diferentes comandos."""