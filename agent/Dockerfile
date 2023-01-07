FROM python:3.10-slim-bullseye
COPY . /code
WORKDIR /code
RUN pip3 install -r libraries.txt
EXPOSE 5000
CMD python3 /code/agent.py
