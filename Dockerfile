# This is an executable file that will help us containerize our application and open it

## Parent image - install python image in docker file
# we need a slim one based on the size of our application(there are medium, large, extralarge options as well)
FROM python:3.11-slim

## Setting up essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Making Work directory inside the docker container witn name 'app'
WORKDIR /app

## Installing system dependancies & updates
RUN apt-get update && apt-get install -y \
    build-essential \   
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copying ur all contents from local to app (except those in dockerignore)
COPY . .

## Run setup.py
# no cache dir - we want to ignore cache files
# This is going to install requirement files and build our flipkart,utils packages
RUN pip install --no-cache-dir -e .

# Port Mapping done below - 5000 is the port that we used for Flask application
EXPOSE 5000

# Run the app 
CMD ["python", "app.py"]