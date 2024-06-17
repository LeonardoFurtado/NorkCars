FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY . .

# Add this line to ensure the script has executable permissions
RUN chmod +x /code/entrypoint.sh

ENV FLASK_APP=run.py
ENV FLASK_ENV=development

ENTRYPOINT ["./entrypoint.sh"]
