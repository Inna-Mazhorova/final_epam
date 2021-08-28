FROM python:3.8.2-alpine

COPY . /

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "app/main_launch.py"]

