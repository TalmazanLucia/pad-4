CREATE KEYSPACE IF NOT EXISTS clothes_app
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE clothes_app;

CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS clothes (
    id UUID PRIMARY KEY,
    name TEXT,
    size TEXT,
    price DOUBLE,
    stock INT,
    color TEXT,
    brand TEXT,
    material TEXT,
    description TEXT,
    is_available BOOLEAN,
    category_id UUID,
    rating DOUBLE
);
