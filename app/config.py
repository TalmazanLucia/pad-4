import uuid

class Config:
    CASSANDRA_HOSTS = ['cassandra1']
    CASSANDRA_PORT = 9042
    CASSANDRA_KEYSPACE = 'clothes_app'
    NODE_ID = str(uuid.uuid4())
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = 'redis'
    CACHE_REDIS_PORT = 6379
    CACHE_DEFAULT_TIMEOUT = 300
