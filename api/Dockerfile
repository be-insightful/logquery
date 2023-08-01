FROM python:3.9-alpine

COPY . /api/api

WORKDIR /api/api

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m pip install -e .

EXPOSE 5000

CMD ["python","./app/main.py"]