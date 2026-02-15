# Usamos o 3.11 para garantir compatibilidade total com as libs do Google no Linux
FROM python:3.11-slim

# Cria a pasta do app dentro do container
WORKDIR /app

# Copia os requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o seu código
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar (O host 0.0.0.0 é obrigatório para nuvem)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]