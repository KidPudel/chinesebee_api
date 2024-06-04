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

RUN source ./venv/bin/activate && pip install --no-cache-dir -r requirements.txt


FROM python:3.12.2-slim-bookworm as serve-stage

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY default.conf /etc/nginx/conf.d/default.conf

COPY --from=build-stage /app/venv /app/venv

WORKDIR /app

RUN source ./venv/bin/activate

CMD sh -c "uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'"
