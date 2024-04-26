# Imagem Base: python:3.9
FROM python:3.8-slim

# Diretorio dentro da imagem que vamos trabalhar
WORKDIR /code

# Copia o arquivo requirements.txt para dentro da imagem
COPY ./requirements.txt /code/requirements.txt

# Instala as dependencias do projeto
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia o conteudo do diretorio atual para dentro da imagem
COPY . /code

# Expoe a porta 80
EXPOSE 5000

# Executa o comando python main.p
CMD ["python", "main.py"]