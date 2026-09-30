#FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt


FROM gcr.io/distroless/python3-debian12

WORKDIR /app

COPY --from=builder /app/deps /app/deps
COPY app/ ./app/
COPY railway_start.py .

ENV PYTHONPATH=/app/deps
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER nonroot

EXPOSE 8000

ENTRYPOINT ["python", "/app/railway_start.py"]
