FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install -r --no-cache-dir requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN adduser --disabled-password --no-create-home fastapiuser

COPY --from=builder /install /usr/local

COPY . .

RUN chown -R appuser:appuser /app

USER fastapiuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]