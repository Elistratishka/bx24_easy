FROM python:3.10

RUN mkdir "/usr/src/app/"

WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

ENV WEBHOOK = "your weebhook here"

CMD ["python", "bx24.py"]
