import os
import platform

def detect_os():
    """Detects the operating system type."""
    os_info = platform.system().lower()
    distro = ""
    
    if os_info == "linux":
        distro = os.popen("cat /etc/os-release | grep '^ID=' | cut -d '=' -f2").read().strip()
    
    return distro

def install_docker(distro):
    print("Updating system packages...")
    os.system("sudo apt update -y" if distro == "ubuntu" else "sudo yum update -y")

    print("Installing required dependencies...")
    if distro == "ubuntu":
        os.system("sudo apt install -y ca-certificates curl gnupg lsb-release")
        os.system("sudo mkdir -p /etc/apt/keyrings")
        os.system("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.gpg > /dev/null")
        os.system("echo \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null")
        os.system("sudo apt update -y && sudo apt install -y docker-ce docker-ce-cli containerd.io")
    else:
        os.system("sudo yum install -y yum-utils device-mapper-persistent-data lvm2")
        os.system("sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo")
        os.system("sudo yum install -y docker-ce docker-ce-cli containerd.io")

    print("Starting and enabling Docker service...")
    os.system("sudo systemctl start docker")
    os.system("sudo systemctl enable docker")

    print("Verifying Docker installation...")
    os.system("docker --version")

def install_docker_compose(distro):
    print("Downloading Docker Compose...")
    os.system("sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose")

    print("Setting executable permissions...")
    os.system("sudo chmod +x /usr/local/bin/docker-compose")

    print("Verifying Docker Compose installation...")
    os.system("docker-compose --version")

def install_and_upgrade_pip(distro):
    print("Installing pip...")
    os.system("sudo apt install -y python3-pip" if distro == "ubuntu" else "sudo yum install -y python3-pip")

    print("Upgrading pip...")
    os.system("sudo pip install --upgrade pip")

def create_and_change_directory():
    folder_name = "docker-projects"

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print(f"Folder '{folder_name}' created successfully!")
    else:
        print(f"Folder '{folder_name}' already exists.")

    os.chdir(folder_name)
    print(f"Changed working directory to '{folder_name}'!")

def create_project_files():
    files = {
        "app.py": """from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

def get_redis_connection():
    try:
        return redis.Redis(
            host=os.getenv('REDIS_HOST', 'redis'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            socket_timeout=5,
            decode_responses=True
        )
    except redis.RedisError as e:
        app.logger.error(f"Redis connection error: {e}")
        return None

cache = get_redis_connection()
if cache is None:
    app.logger.warning("Proceeding without Redis connection.")

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
      - REDIS_HOST=redis
      - DEBUG=true

  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"
""",

        "Dockerfile": """# Use the official Python image
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

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
    distro = detect_os()
    if distro not in ["ubuntu", "centos", "rhel"]:
        print(f"Unsupported OS detected: {distro}. This script works on Ubuntu and Red Hat-based distros.")
    else:
        install_docker(distro)
        install_docker_compose(distro)
        install_and_upgrade_pip(distro)
        print("Docker, Docker Compose, and pip setup completed!")

        create_and_change_directory()
        create_project_files()
        print("Project directory and files setup completed!")
