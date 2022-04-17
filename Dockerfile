FROM python:3.9.7

ADD main.py .
ADD structure.py .

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]
