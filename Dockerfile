FROM python:3.11-slim

WORKDIR /app
COPY inventory.py client.py ./

ENV PYTHONUNBUFFERED=1

CMD ["python3", "inventory.py"]
