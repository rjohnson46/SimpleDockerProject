from flask import Flask, jsonify
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

if __name__ == "__main__":
    # Use 0.0.0.0 to ensure the app is accessible from outside the container
    app.run(host='0.0.0.0', port=int(os.getenv('APP_PORT', 5000)))