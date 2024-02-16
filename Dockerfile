FROM python:3.10

WORKDIR /usr/src/app

EXPOSE 8000

COPY ./djangonote .
COPY ./requre.txt .
COPY ./buildup.sh /

RUN pip install psycopg2-binary
RUN pip install -r requre.txt

ENTRYPOINT [ "/bin/bash", "/buildup.sh" ]