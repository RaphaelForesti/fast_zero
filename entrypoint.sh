#!/bin/sh

# Aplica as migrações do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação FastAPI com Uvicorn
poetry run uvicorn fast_zero.app:app --host 0.0.0.0 --port 8000
