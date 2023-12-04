# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables to not generate pyc files and to unbuffer Python output,
# which is useful in a Docker context to see the output of your application in real time
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the Docker image
WORKDIR /code

# Install system dependencies
# This includes packages that are necessary for Django to run as well as tools like
# netcat which can be used to check if the database is up and running
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && apt-get clean

# Upgrade pip and install Python dependencies
# Copy the requirements file from your project and install the Python packages
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your Django application into the Docker image
COPY . /code/

# Copy the entrypoint script into the image and make sure it's executable
COPY entrypoint.sh /code/
RUN chmod +x /code/entrypoint.sh

# Expose the port your app runs on
EXPOSE 8000

COPY entrypoint.sh /code/

# Ensure the script is executable
RUN chmod +x /code/entrypoint.sh