FROM python:3.4.8-alpine

# LABEL Vikas Kumar "vikas@reachvikas.com"

RUN apk update && \
    apk add --update --no-cache g++ gcc libxslt-dev && \
    rm -rf /var/cache/apk/* /tmp/requirements.txt

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
ADD . .

CMD /app/app.py
