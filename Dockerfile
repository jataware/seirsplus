FROM python:3.8

RUN apt-get update && apt-get install -y \
  python3-pip \
  git \
  vim 


WORKDIR /
RUN git clone https://github.com/jataware/seirsplus.git

WORKDIR /seirsplus/
COPY . .
RUN pip3 install -r requirements.txt


ENTRYPOINT ["python3", "src/seirs.py"]
CMD ["iso2=ET", "-startDate=2020-11-01", "-endDate=2020-11-30", "-simDays=31"]