# Stage 1: install dependencies using a full Python image (has pip, compilers, etc.)
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

# Stage 2: final runtime image - distroless, no shell, no package manager, no pip
FROM gcr.io/distroless/python3-debian12
WORKDIR /app
COPY --from=builder /app/deps /app/deps
COPY app/ ./app/
ENV PYTHONPATH=/app/deps
USER nonroot
EXPOSE 8000
ENTRYPOINT ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
