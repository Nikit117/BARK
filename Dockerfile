
FROM python:3.8-slim

WORKDIR /app
COPY ./main.py /app/main.py
COPY ./requirements.txt /app/requirements.txt

#install git/pip 
RUN apt-get update && \
	apt-get install -y git && \
	pip install --no-cache-dir -r requirements.txt && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

EXPOSE 8000

#uvicorn server
CMD ["uvicorn","main:app","--reload","--host 0.0.0.0","--port","8000"]