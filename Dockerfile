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

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3.12.2-slim-bookworm AS serve-stage


RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y --no-install-recommends \
    build-essential \
    nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY default.conf /etc/nginx/conf.d/default.conf

COPY --from=build-stage /app/wheels ./wheels

# use pre-build dependencies
RUN pip install --no-cache ./wheels/*

COPY . .

EXPOSE 80

CMD sh -c "uvicorn main:app --host 127.0.0.1 --port 8000 & nginx -g 'daemon off;'"
