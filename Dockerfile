# Shiplon test app: Dockerfile runtime.
# Shiplon runs apps as non-root, so the image must set a NUMERIC user (USER 10001,
# not USER appuser): Kubernetes can only verify a numeric user isn't root.
FROM python:3.13-alpine

WORKDIR /app
COPY app.py .

ENV PYTHONUNBUFFERED=1 PORT=8080
EXPOSE 8080
USER 10001

CMD ["python", "app.py"]
