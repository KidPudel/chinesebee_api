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

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

FROM python:3.12.2-slim-bookworm AS serve-stage

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY default.conf /etc/nginx/conf.d/default.conf

COPY --from=build-stage /app /app

WORKDIR /app

RUN pip install uvicorn

EXPOSE 80 8000

CMD uvicorn main:app --host 0.0.0.0 --port 8000 & nginx -g 'daemon off;'