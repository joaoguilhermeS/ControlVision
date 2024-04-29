FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

ENV OPENAI_API_KEY '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'

RUN apt-get update -y && \
    apt-get install -y sqlite3 && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python3", "api.py"]