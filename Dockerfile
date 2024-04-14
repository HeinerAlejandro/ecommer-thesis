FROM python:3.10-slim-bullseye as base

ENV DOCKER_CONTENT_TRUST=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG PIP_INDEX_URL
ENV PATH="/opt/venv/bin:$PATH"

FROM base as build

WORKDIR /app

RUN python -m venv /opt/venv

COPY requirements.txt .
RUN apt-get -y update && apt-get -y install gcc libpq-dev python3-dev && /opt/venv/bin/pip install -r requirements.txt


FROM base as app

WORKDIR /home/app
COPY entrypoint.sh /home/app/
COPY ./datasets .

RUN chmod +x /home/app/entrypoint.sh


COPY . .

COPY --from=build /opt/venv /opt/venv
ENTRYPOINT [ "/home/app/entrypoint.sh" ]
