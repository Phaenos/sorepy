FROM python:3.9-slim

WORKDIR /sorepy

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

VOLUME /data

EXPOSE 5000

RUN groupadd -r sorepy && useradd --no-log-init -r -g sorepy sorepy
USER sorepy:sorepy

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "sorepy:app"]
