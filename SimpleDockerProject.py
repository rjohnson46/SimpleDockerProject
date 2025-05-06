import os

def install_docker():
    print("Updating system packages...")
    os.system("sudo yum update -y")

    print("Installing required dependencies...")
    os.system("sudo yum install -y yum-utils device-mapper-persistent-data lvm2")

    print("Adding Docker repository...")
    os.system("sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo")

    print("Installing Docker...")
    os.system("sudo yum install -y docker-ce docker-ce-cli containerd.io")

    print("Starting and enabling Docker service...")
    os.system("sudo systemctl start docker")
    os.system("sudo systemctl enable docker")

    print("Verifying Docker installation...")
    os.system("docker --version")


def install_docker_compose():
    print("Downloading Docker Compose...")
    os.system("sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose")

    print("Setting executable permissions...")
    os.system("sudo chmod +x /usr/local/bin/docker-compose")

    print("Verifying Docker Compose installation...")
    os.system("docker-compose --version")


def install_and_upgrade_pip():
    print("Installing pip...")
    os.system("sudo yum install -y python3-pip")

    print("Upgrading pip...")
    os.system("sudo pip install --upgrade pip")


def create_and_change_directory():
    folder_name = "docker-projects"

    # Create the folder if it doesn't already exist
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' created successfully!")
    else:
        print(f"Folder '{folder_name}' already exists.")

    # Change the working directory to the newly created folder
    os.chdir(folder_name)
    print(f"Changed working directory to '{folder_name}'!")


def create_project_files():
    files = {
        "app.py": """from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

# Connect to Redis with error handling
def get_redis_connection():
    try:
        return redis.Redis(
            host=os.getenv('REDIS_HOST', 'redis'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            socket_timeout=5,
            decode_responses=True  # Ensure Redis responses are decoded to strings
        )
    except redis.RedisError as e:
        app.logger.error(f"Redis connection error: {e}")
        return None

cache = get_redis_connection()
if cache is None:
    app.logger.warning("Proceeding without Redis connection. Some features may not work.")

@app.route('/')
def hello():
    if cache is None:
        return jsonify({"error": "Unable to connect to Redis"}), 500

    try:
        count = cache.incr('visits')
        return jsonify({"message": f"Hello, World! You have visited {count} times."})
    except redis.RedisError as e:
        app.logger.error(f"Redis operation error: {e}")
        return jsonify({"error": "Redis operation failed"}), 500

# Use 0.0.0.0 to ensure the app is accessible from outside the container
try:
    app.run(host='0.0.0.0', port=int(os.getenv('APP_PORT', 5000)))
except Exception as e:
    app.logger.error(f"Application failed to start: {e}")
""",

        "docker-compose.yml": """version: '3'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis  # Correct format: "KEY=VALUE"
      - ANOTHER_VAR=some_value
      - DEBUG=true

  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"
""",

        "Dockerfile": """# Use the official Python image
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
""",

        "requirements.txt": """Flask
redis
"""
    }

    for filename, content in files.items():
        with open(filename, "w") as file:
            file.write(content)
        print(f"File '{filename}' created successfully!")

    print("All project files have been created successfully!")


if __name__ == "__main__":
    install_docker()
    install_docker_compose()
    install_and_upgrade_pip()
    print("Docker, Docker Compose, and pip installation/upgradation completed successfully!")

    create_and_change_directory()
    create_project_files()
    print("Project directory and files setup completed successfully!")
