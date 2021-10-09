FROM python:3.8-slim

COPY spotify_client/requirements*.txt /tmp/
RUN pip install -r /tmp/requirements.txt -r /tmp/requirements.plotly.txt
