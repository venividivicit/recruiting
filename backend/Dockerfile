FROM rust:1.84 AS builder

WORKDIR /queries
COPY queries .
RUN cargo clean
RUN cargo build --release

FROM python:3.12

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY . .

# Copy compiled Rust binary
RUN mkdir -p /queries/target/release
COPY --from=builder /queries/target/release/sedaro-nano-queries /queries/target/release/sedaro-nano-queries

# Run FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]