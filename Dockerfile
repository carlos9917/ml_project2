#FROM python:3.8.12-slim
#FROM agrigorev/zoomcamp-model:3.8.12-slim
FROM python:3.9-slim

RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

#this one will install it in the system using the pipfile above
RUN pipenv install --system --deploy

COPY ["main.py", "random_forest.bin", "./"]
COPY ["app", "./app"]
#expose the port 9696
EXPOSE 9696

#ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "webserver:app"]
ENTRYPOINT ["python", "main.py"]
#ENTRYPOINT ["uvicorn", "main:app", "host:0.0.0.0","--reload"]
#ENTRYPOINT ["uvicorn", "app.app:app", "--reload"]
#ENTRYPOINT ["uvicorn", "app.app:app",  "--host=0.0.0.0:8800","--reload"]
#CMD ["uvicorn", "app.app:app",  "--host=0.0.0.0:8800","--reload"]
#ENTRYPOINT ["uvicorn", "./main:app", "--host=0.0.0.0:8800","--reload"]
#ENTRYPOINT ["uvicorn", "app.app:app", "--host=0.0.0.0:9696","--reload"]
#CMD ["echo Hello"]
