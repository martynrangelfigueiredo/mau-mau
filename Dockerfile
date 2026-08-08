# Multi-stage Dockerfile for Mau-Mau Web Application (Kubernetes Ready)
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Copy project files and install dependencies
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/
COPY tests/ ./tests/

RUN pip install --no-cache-dir . pytest


# Production Runtime Stage
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

# Set non-root user for security
RUN useradd -m -u 1000 maumau && chown -R maumau:maumau /app
USER maumau

ENV PORT=8000
EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["python3", "-m", "maumau.server"]
