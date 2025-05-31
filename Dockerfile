FROM python:3.10-slim

WORKDIR /app

COPY App/ ./App/
COPY Requirements.txt .

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r Requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "App/StreamlitApp.py", "--server.port=8501", "--server.address=0.0.0.0"]