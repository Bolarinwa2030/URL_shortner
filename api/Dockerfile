FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

#STAGE 2
FROM python:3.12-slim AS runtime

#RUN as non-root user
RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser/app


COPY --from=builder /install /usr/local

COPY --chown=appuser:appuser app/ ./app/

EXPOSE 8000

# HEALTHCHECK if container are fine

HEALTHCHECK --interval=30s --timeout=30s --start-period=10s \
CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]

