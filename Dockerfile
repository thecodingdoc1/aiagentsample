
FROM public.ecr.aws/lambda/python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY .env db_setup.py agent.py main.py requirements.txt .
CMD ["python", "main.py"]