
# Demo-only Dockerfile for cfo-router
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
ENV ROUTER_BIND=0.0.0.0
ENV ROUTER_PORT=8001
EXPOSE 8001
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
