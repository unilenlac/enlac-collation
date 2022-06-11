FROM ubuntu:latest
RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -q -y python3-pip

RUN pip3 install unidecode

COPY . ../enlac-collation/

#RUN useradd -u 8877 unilenlac

#USER unilenlac

COPY shell-scripts/main.sh /bin/main.sh

WORKDIR /home/

CMD /bin/main.sh /home
