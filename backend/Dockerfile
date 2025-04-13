FROM python:3.10
WORKDIR ~
COPY . .

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]