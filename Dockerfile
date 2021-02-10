FROM alpine:3.7

WORKDIR /usr/src/pydango-pip

COPY requirements.txt .

RUN \
  apk add --no-cache libffi-dev && \
  apk add --no-cache python3 postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
  python3 -m pip install --upgrade pip && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

COPY . .

CMD ["python3", "-m", "pydango", "-d", "sqlite"]



