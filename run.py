import threading
import time
import redis
from app import create_app

# Create Flask app
app = create_app()

# Initialize Redis client
redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

# Unique Node ID from Config
node_id = app.config.get('NODE_ID', 'unknown_node')

def send_heartbeat():
    """Periodically send heartbeat to Redis."""
    try:
        while True:
            redis_client.set(f"node:{node_id}:heartbeat", "alive", ex=15)  # Expiry time = 15 seconds
            print(f"Heartbeat sent for node: {node_id}")
            time.sleep(5)  # Send heartbeat every 5 seconds
    except Exception as e:
        print(f"Error in heartbeat thread: {e}")

def run_flask_app():
    """Run the Flask application."""
    try:
        print("Starting Flask app...")
        app.run(host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"Error in Flask app: {e}")

if __name__ == '__main__':
    # Start the heartbeat thread
    heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)
    heartbeat_thread.start()

    # Start the Flask application
    run_flask_app()
