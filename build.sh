#!/usr/bin/env bash
# Comandos executados pelo Render a cada deploy.
# Sai no primeiro erro, para um deploy quebrado não subir silenciosamente.
set -o errexit

pip install -r requirements.txt

# Junta os arquivos estáticos numa pasta só, para o WhiteNoise servir.
python manage.py collectstatic --no-input

# Cria/atualiza as tabelas no PostgreSQL do Render.
python manage.py migrate

# Carrega as anotações de exemplo. O fixture tem as chaves primárias fixas,
# então rodar de novo atualiza os mesmos registros em vez de duplicá-los.
python manage.py loaddata dados-iniciais.json
