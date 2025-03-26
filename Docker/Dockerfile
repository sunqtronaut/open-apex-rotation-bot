FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/dependencies -r requirements.txt

FROM gcr.io/distroless/python3

WORKDIR /app

COPY --from=builder /app/dependencies /app/dependencies
COPY . .

ENV PYTHONPATH=/app/dependencies

CMD ["main-tg.py"]
