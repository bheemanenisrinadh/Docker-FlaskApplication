FROM python:3.11-slim
LABEL maintainer="SREENADH"
LABEL description="my docker file practise"
LABEL version="1.0"
COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app
COPY . /app
RUN
ENV FLASK_ENV=production 
ENV PORT=8000
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=2).status==200 else 1)"
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "wsgi:app"]
