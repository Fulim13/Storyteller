FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/api

COPY requirements.txt /app/api/


# Build psycopg2-binary from source -- add required required dependencies
RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc python3-dev musl-dev && \
    # pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 && \
    pip install --no-cache-dir -r requirements.txt && \
    apk --purge del .build-deps

COPY . /app/api/

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

EXPOSE 8000
