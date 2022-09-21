FROM python:3.10

COPY src/ app/
WORKDIR /app

RUN pip install -r requirements.txt

ENV TELETHON_API_ID id
ENV TELETHON_API_HASH hash
ENV TELETHON_PHONE phone
ENV TELETHON_BOT_TOKEN bottoken
ENV TELETHON_SUBMANAGER_BOT_TOKEN submanagerbottokken
ENV CLOUD_HOST 1

CMD ["python" ,"main.py"]