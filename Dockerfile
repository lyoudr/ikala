FROM python:3.8-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /ann

COPY . /ann/
RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "/ann/entrypoint.sh"]