# Base image
FROM python:alpine3.20

# Copy all files from flask_api to app in image
COPY ./flask_api /app

# Change dir (CD)
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Open port 420
EXPOSE 420

# Start command when container runs
CMD [ "python", "app.py" ]

