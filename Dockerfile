FROM python:3.10

WORKDIR /app/

COPY ./app/requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
ENV PYTHONPATH=/app

RUN chmod +x start.sh

CMD ["./start.sh"]