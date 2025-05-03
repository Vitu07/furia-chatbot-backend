import subprocess
import time
import os

# Inicia o servidor de ações em segundo plano
print("Iniciando o servidor de ações...")
actions_process = subprocess.Popen(["rasa", "run", "actions"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Espera alguns segundos para garantir que as actions subam primeiro
time.sleep(5)

# Inicia o servidor principal da API Rasa
print("Iniciando o servidor principal...")
os.system("rasa run --enable-api --cors \"*\" --port 12000")
