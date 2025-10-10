FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]