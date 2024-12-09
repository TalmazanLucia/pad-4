from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from cassandra.cluster import Cluster
from app.config import Config
import time
import cassandra

cache = Cache()  # Initialize cache at the module level
cluster = None   # Initialize cluster at the module level
session = None   # Initialize session at the module level

def create_app():
    global cluster, session, cache # Declare globals to modify them inside the function
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('app.config.Config')

    # Initialize cache with app
    cache.init_app(app, config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_REDIS_URL': 'redis://redis:6379/0'
    })

    # Cassandra connection setup
    def connect_to_cassandra():
        max_retries = 10
        for attempt in range(max_retries):
            try:
                cluster = Cluster(Config.CASSANDRA_HOSTS, port=Config.CASSANDRA_PORT)
                session = cluster.connect('clothes_app')
                print("Connected to Cassandra")
                return cluster, session
            except cassandra.cluster.NoHostAvailable as e:
                print(f"Cassandra not available, retrying ({attempt + 1}/{max_retries})...")
                time.sleep(5)
            except cassandra.DriverException as e:
                print(f"Driver exception occurred: {e}")
                time.sleep(5)
            except Exception as e:
                print(f"Unexpected exception: {e}")
                time.sleep(5)
        raise Exception("Failed to connect to Cassandra after retries")

    # Initialize Cassandra cluster and session
    cluster, session = connect_to_cassandra()

    CORS(app)

    # Register blueprints
    from app.routes.clothes import clothes_bp
    from app.routes.categories import categories_bp
    from app.routes.health import health_bp
    from app.routes.status import status_bp

    app.register_blueprint(clothes_bp, url_prefix='/api/clothes')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    app.register_blueprint(status_bp, url_prefix='/api/status')

    return app
