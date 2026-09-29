# This Dockerfile creates the flasktest image used in the container experiment.
# It sets up a Python environment, copies app.py into the image, installs Flask
# and Gunicorn, and starts the application with Gunicorn on port 8000.
# Each of the 20 containers runs its own copy of the application from this image.

FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN pip install flask gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--threads", "1", "app:create_app()"]
