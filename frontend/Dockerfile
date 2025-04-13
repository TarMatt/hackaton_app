FROM python:3.10
WORKDIR ~
COPY . .

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root
ENTRYPOINT ["streamlit", "run", "frontend.py", "--server.port=8555", "--server.address=0.0.0.0"]