FROM python:3-slim

WORKDIR /sorepy

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

VOLUME /sorepy/data/

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "sorepy:app"]
