FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8050

ENV REDIS_HOST=redis

CMD ["python", "app.py"]