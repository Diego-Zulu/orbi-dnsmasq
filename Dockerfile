FROM python:3.8-alpine3.12

RUN pip install requests

ADD . /orbi_dnsmasq
WORKDIR /orbi_dnsmasq
RUN python setup.py install

RUN addgroup -S orbi && adduser -S orbi -G orbi
USER orbi

ENTRYPOINT ["orbi-dnsmasq"]
