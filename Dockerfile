# Use the official Python image from the DockerHub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /code/

# Add a non-root user
RUN adduser --disabled-password --gecos '' django_user
USER django_user

# Expose the port the app runs on
EXPOSE 8000

# Command to run on container start (using Django's built-in server)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
