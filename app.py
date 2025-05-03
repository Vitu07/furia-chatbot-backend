import subprocess
import time
import os

# Pega a porta da variável de ambiente (Render fornece automaticamente)
port = os.environ.get("PORT", 10000)

# Inicia o servidor de ações
print("Iniciando o servidor de ações...")
subprocess.Popen(["rasa", "run", "actions"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Espera o servidor de ações iniciar
time.sleep(5)

# Inicia o servidor principal na porta fornecida pelo Render
print(f"Iniciando o servidor principal na porta {port}...")
os.system(f"rasa run --enable-api --cors '*' --port {port}")
