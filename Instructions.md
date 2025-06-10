
# 🐳 Building a Simple "Hello World" Docker Project

🚀 In this guide, we'll create a containerized Python web application that displays a "Hello World" message. This tutorial works on Ubuntu/Debian-based Linux distros and is optimized for Hashnode with proper formatting and code blocks.

---

## 🔹 System Preparation

Before we start, update and upgrade your system packages:

```bash
sudo apt update
sudo apt upgrade -y
```

Install Docker and other required dependencies:

```bash
sudo apt install ca-certificates curl gnupg
```

### Add Docker’s Official GPG Key

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

### Add Docker Repository

```bash
echo "deb [signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Install Docker

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Verify installation:

```bash
docker --version
```

Start and enable Docker:

```bash
sudo systemctl enable --now docker
```

Check Docker status:

```bash
sudo systemctl status docker
```

---

## 🔹 Install Docker Compose Plugin

Ubuntu now uses the Docker Compose plugin instead of the standalone binary:

```bash
sudo apt install docker-compose-plugin -y
```

Verify installation:

```bash
docker compose version
```

Install Python Pip for dependencies:

```bash
sudo apt install python3-pip
python3 -m pip install --upgrade pip
```

---

## 🔹 Create Project Directory

Set up the directory structure:

```bash
mkdir docker-projects
cd docker-projects
```

---

## 🔹 Create Python Web Application

Create the `app.py` file:

```bash
touch app.py
nano app.py
```

Copy & paste the following Python Flask app:

```python
from flask import Flask
import redis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    try:
        return cache.incr('hits')
    except redis.exceptions.ConnectionError:
        return 1

@app.route('/')
def hello():
    count = get_hit_count()
    return f"Hello World! You have visited {count} times."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Save the file (`CTRL + X`, then `Y`).

---

## 🔹 Define Dependencies

Create the `requirements.txt` file:

```bash
touch requirements.txt
nano requirements.txt
```

Add dependencies inside `requirements.txt`:

```
Flask
redis
```

Save (`CTRL + X`, then `Y`).

---

## 🔹 Create Dockerfile

Create a `Dockerfile`:

```bash
touch Dockerfile
nano Dockerfile
```

Paste the following Dockerfile configuration:

```dockerfile
FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

Save (`CTRL + X`, then `Y`).

---

## 🔹 Configure Docker Compose

Create the `docker-compose.yml` file:

```bash
touch docker-compose.yml
nano docker-compose.yml
```

Paste the Docker Compose config:

```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    depends_on:
      - redis

  redis:
    image: "redis:alpine"
```

Save (`CTRL + X`, then `Y`). ⚠ YAML files are sensitive to indentation—validate them before running!

---

## 🔹 Build and Run the Project

Ensure you're in the `docker-projects` directory:

```bash
cd docker-projects
```

Start the containers:

```bash
sudo docker-compose up --build
```

---

## 🔹 Test the Web App

Open a browser and go to [http://localhost:5000](http://localhost:5000).

You should see:

```
Hello World! You have visited 1 times.
```

Refreshing the page will increase the visitor count.

---

## 🔹 Stop Containers

Shut down the containers when you're done:

```bash
sudo docker-compose down
```

