# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app to the container
COPY . /app

# Expose port 5000
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]