FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml .
COPY z7scan/ ./z7scan/
RUN pip install -e . --no-cache-dir
CMD ["python", "-c", "import z7scan; print('z7scan', z7scan.__version__ if hasattr(z7scan, '__version__') else 'ready')"]
