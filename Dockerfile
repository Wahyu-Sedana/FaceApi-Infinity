FROM python:3.9

WORKDIR /face
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]