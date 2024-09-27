# Base image
FROM python:alpine3.20

# Copy all files from flask_api to app in Docker image
COPY . /app

# Change dir (CD)
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Open port 420
EXPOSE 420

# Start command when container runs
CMD [ "python", "app.py" ]

