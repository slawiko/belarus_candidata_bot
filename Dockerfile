FROM python:3.7-alpine

RUN apk --no-cache add gcc musl-dev libffi-dev openssl-dev python3-dev

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./telegram_bot.py ./
COPY ./src ./

COPY ./candidates ./

ENTRYPOINT ["/usr/local/bin/python", "telegram_bot.py"]
