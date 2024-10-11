# Base image
FROM python:alpine3.20

# Copy to app dir
COPY . /app

# Change dir
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Start cmd
CMD [ "python", "app.py" ]
