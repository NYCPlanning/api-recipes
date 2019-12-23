FROM sptkl/cook:latest

WORKDIR /usr/src/app

COPY . .

RUN pip3 install -r requirements.txt

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]

EXPOSE 5000