FROM python:3.13-slim

# Configurar o Poetry para não criar ambientes virtuais
ENV POETRY_VIRTUALENVS_CREATE=false

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . .

# Instala o Poetry
RUN pip install poetry

# Configurações do Poetry para otimizar a instalação
RUN poetry config installer.max-workers 10

# Instala as dependências do projeto
RUN poetry install --no-interaction --no-ansi

# Torna o arquivo entrypoint.sh executável (se necessário)
RUN chmod +x /app/entrypoint.sh

# Expõe a porta 8000
EXPOSE 8000

# Define o entrypoint para o script de inicialização
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
