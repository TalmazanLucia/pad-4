import redis
import time

redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

def monitor_nodes():
    """Monitor heartbeat status of all nodes."""
    while True:
        keys = redis_client.keys("node:*:heartbeat")
        print(f"Active nodes ({len(keys)}):")
        for key in keys:
            node_id = key.split(":")[1]
            print(f" - {node_id} is alive")
        time.sleep(10)

if __name__ == '__main__':
    monitor_nodes()
