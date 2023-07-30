FROM python:3.10

RUN pip install gradio openai-async

WORKDIR /app

COPY simple_request3.py /app

CMD ["python", "simple_request3.py"]