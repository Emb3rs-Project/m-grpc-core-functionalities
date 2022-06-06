FROM python:3.10-slim as compile

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y build-essential gcc

RUN python -m venv /opt/venv
ENV PATH='/opt/venv/bin:$PATH'

WORKDIR /usr/src/app
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

FROM python:3.10-slim as build

# setup config
ENV GROUP_ID=1000 \
    USER_ID=1000

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

COPY --from=compile /opt/venv /opt/venv
ENV PATH='/opt/venv/bin:$PATH'

# Configuring app
WORKDIR /app
COPY . .

ENV PYTHONPATH=ms_grpc/plibs

EXPOSE 50051

CMD [ "python", "-u" , "server.py" ]