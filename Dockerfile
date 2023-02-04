FROM python:3.10-alpine
COPY ./project /app
WORKDIR /app
ENV PYTHONPATH=/app
RUN pip3 install -r /app/requirements.txt
CMD python3 /app/RUN_TELEGRAM_S3.py