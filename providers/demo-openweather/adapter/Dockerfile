FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn httpx
EXPOSE 8080
CMD ["uvicorn","app:APP","--host","0.0.0.0","--port","8080"]
