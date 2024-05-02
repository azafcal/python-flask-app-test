# syntax=docker/dockerfile:experimental

##
# PYTHON - APP - DOCKER IMAGE - 2024-04-10
#
FROM python:3.6-slim

# Set working directory
WORKDIR /app

# Set PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Copy the source code into the container
COPY ./requirements.txt /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#COPY ./src ./src

# Specify the command to run on container startup
CMD ["python3","apptest.py"]
