import subprocess
import os

def run_command(command):
    """Run a shell command and print output."""
    print(f"Executing: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Error: {result.stderr}")
        exit(1)

def setup_system():
    """Update and upgrade the system."""
    print("Updating and upgrading system...")
    run_command("sudo apt update && sudo apt upgrade -y")

def install_docker():
    """Install Docker."""
    print("Installing Docker...")
    run_command("sudo apt install -y ca-certificates curl gnupg")
    run_command("sudo install -m 0755 -d /etc/apt/keyrings")
    run_command("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null")
    run_command("sudo chmod a+r /etc/apt/keyrings/docker.asc")
    ubuntu_version = subprocess.run("lsb_release -cs", shell=True, capture_output=True, text=True).stdout.strip()
    run_command(f'echo "deb [signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu {ubuntu_version} stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
    run_command("sudo apt update")
    run_command("sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")
    run_command("sudo docker run hello-world")

def install_docker_compose():
    """Install Docker Compose."""
    print("Installing Docker Compose...")
    run_command('sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose')
    run_command("sudo chmod +x /usr/local/bin/docker-compose")
    run_command("docker-compose --version")

def install_tools():
    """Install Nano, Pip, and upgrade Pip."""
    print("Installing Nano, Pip, and upgrading Pip...")
    run_command("sudo apt install -y nano")
    run_command("sudo apt install -y python3-pip")
    run_command("sudo pip3 install --upgrade pip")

def setup_project_directory():
    """Set up project directory."""
    print("Setting up project directory...")
    run_command("mkdir -p ~/docker-projects")
    os.chdir(os.path.expanduser("~/docker-projects"))

def create_files():
    """Create necessary project files."""
    print("Creating project files...")
    files = {
        "app.py": """\
from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

def get_redis_connection():
    try:
        return redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, decode_responses=True)
    except redis.RedisError as e:
        app.logger.error(f"Redis connection error: {e}")
        return None

cache = get_redis_connection()

@app.route('/')
def hello():
    if cache:
        count = cache.incr('visits')
        return jsonify({"message": f"Hello, World! You have visited {count} times."})
    return jsonify({"error": "Unable to connect to Redis"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
""",
        "requirements.txt": "Flask\nredis",
        "Dockerfile": """\
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 5000
CMD ["python", "app.py"]
""",
        "docker-compose.yml": """\
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"
"""
    }

    for filename, content in files.items():
        with open(filename, "w") as f:
            f.write(content)

def build_and_run():
    """Build and run the Docker project."""
    print("Building and running the Docker project...")
    run_command("sudo docker-compose up --build")

def cleanup():
    """Stop and remove the containers."""
    print("Stopping and removing containers...")
    run_command("sudo docker-compose down")

if __name__ == "__main__":
    setup_system()
    install_docker()
    install_docker_compose()
    install_tools()
    setup_project_directory()
    create_files()
    build_and_run()
