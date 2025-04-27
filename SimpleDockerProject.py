import subprocess
import os

def run_command(command, check=True):
    """
    Executes a shell command.

    Args:
        command (str): The command to execute.
        check (bool, optional): If True, raises a CalledProcessError if the command fails. Defaults to True.
    """
    try:
        print(f"Executing: {command}")
        subprocess.run(command, shell=True, check=check)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        if check:
            raise  # Re-raise the exception if check is True
        #If check is false, the function will continue to execute

def main():
    """
    Runs the series of commands for the SimpleDockerProject setup.
    """
    try:
        # Update and upgrade system packages
        run_command("sudo apt update -y")
        run_command("sudo apt upgrade -y")

        # Install Docker and Docker Compose
        run_command("sudo apt install docker.io -y")
        run_command("sudo apt install docker-compose -y") #may need to install via curl

        # Install Nano and Pip
        run_command("sudo apt install nano -y")
        run_command("sudo apt install python3-pip -y")
        run_command("sudo python3 -m pip install --upgrade pip")

        # Create project directory and change to it
        run_command("mkdir -p docker-projects")
        os.chdir("docker-projects")
        #run_command("cd docker-projects") # replaced with os.chdir

        # Create and populate app.py
        run_command("touch app.py")
        app_py_content = """
from flask import Flask
import redis
import os

app = Flask(__name__)
cache = redis.Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379)

@app.route('/')
def hello():
    count = cache.incr('visits')
    return f'Hello, World! You have visited {count} times.'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
"""
        with open("app.py", "w") as f:
            f.write(app_py_content)
        #removed sudo nano, as we are writing the file

        # Create and populate requirements.txt
        run_command("touch requirements.txt")
        requirements_content = "Flask\\nredis\\n"
        with open("requirements.txt", "w") as f:
            f.write(requirements_content)
        #removed sudo nano, as we are writing the file

        # Create Dockerfile
        run_command("touch dockerfile")
        dockerfile_content = """
FROM python:3.9-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
"""
        with open("Dockerfile", "w") as f:
            f.write(dockerfile_content)
        #removed sudo nano, as we are writing the file

        # Create and populate docker-compose.yml
        run_command("touch docker-compose.yml")
        docker_compose_content = """
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - redis
  redis:
    image: "redis:latest"
"""
        with open("docker-compose.yml", "w") as f:
            f.write(docker_compose_content)
        #removed sudo nano, as we are writing the file

        # Change to the project directory (redundant, but kept for clarity)
        os.chdir("docker-projects")

        # Build and start the Docker containers
        run_command("sudo docker-compose up --build", check=False) #changed check to false, so script doesnt stop

        print("Simple Docker Project setup complete.  To stop the containers, run 'sudo docker-compose down'")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Simple Docker Project setup incomplete.  Please check the error messages and try again.")

if __name__ == "__main__":
    main()

