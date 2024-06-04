FROM python:3.12.2-slim-bookworm AS build-stage

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    python3-dev \
    linux-headers-generic \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN python -m venv venv

RUN . ./venv/bin/activate && pip install --no-cache-dir -r requirements.txt


FROM python:3.12.2-slim-bookworm as serve-stage

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y --no-install-recommends \
    build-essential \
    nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY default.conf /etc/nginx/conf.d/default.conf

WORKDIR /app

COPY . .

COPY --from=build-stage /app/venv ./venv



CMD sh -c ". /app/venv/bin/activate && uvicorn main:app --host 127.0.0.1 --port 8000 & nginx -g 'daemon off;'"
