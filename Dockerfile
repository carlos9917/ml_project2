#FROM python:3.8.12-slim
#FROM agrigorev/zoomcamp-model:3.8.12-slim
FROM python:3.9-slim

RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

#this one will install it in the system using the pipfile above
RUN pipenv install --system --deploy

#COPY ["weather_data/ikermit.csv.gz", "./"]
COPY ["weather_data/*", "./weather_data/"]
COPY ["predict.py", "*bin", "./"]
COPY ["*.py", "./"]
#COPY ["f_app", "./"]
#expose the port 9999
EXPOSE 9999
ENTRYPOINT ["python", "predict.py"]
