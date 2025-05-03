#!/bin/bash

# =============== DEBUG INICIAL ===============
echo "✅ Script iniciado - Verificando dependências..."
pip list | grep rasa  # Mostra versões instaladas

# =============== INICIA ACTIONS ===============
echo "🔄 Iniciando servidor de Actions na porta 5055..."
python -m rasa_sdk --actions actions --port 5055 &
if [ $? -eq 0 ]; then
    echo "✅ Actions iniciado com sucesso!"
else
    echo "❌ Falha ao iniciar Actions. Verifique actions/actions.py."
    exit 1
fi

# =============== INICIA RASA ===============
echo "🔄 Iniciando Rasa na porta $PORT..."
rasa run \
  --model models \
  --enable-api \
  --cors "*" \
  --port $PORT \
  --debug  # Modo debug do Rasa

# Se o servidor crashar:
echo "❌ Rasa parou inesperadamente. Verifique os logs acima."