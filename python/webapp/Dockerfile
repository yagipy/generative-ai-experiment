FROM python:3.12.2-bookworm

WORKDIR /python/webapp

COPY pyproject.toml poetry.lock ./

ENV POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH" \
    HOST=0.0.0.0

RUN apt update \
    && apt install -y sqlite3 \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry install

CMD poetry run streamlit run webapp/Home.py
