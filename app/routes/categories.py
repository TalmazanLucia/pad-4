from flask import Blueprint, request
import uuid
from app.helper import create_response
from app import session, cache

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('', methods=['GET'])
@cache.cached(timeout=300, key_prefix='all_categories')
def get_categories():
    query = "SELECT id, name FROM categories;"
    rows = session.execute(query)
    categories = [{"id": str(row.id), "name": row.name} for row in rows]
    return create_response(categories, request.headers.get('Accept', 'application/json')), 200

@categories_bp.route('', methods=['POST'])
def add_category():
    data = request.json

    # Validation
    if not data.get("name"):
        return create_response({"error": "Category name is required"}, request.headers.get('Accept', 'application/json')), 400

    query = "INSERT INTO categories (id, name) VALUES (%s, %s);"
    category_id = uuid.uuid4()
    session.execute(query, (category_id, data.get("name")))

    # Clear the cache when a new category is added
    cache.delete('all_categories')

    return create_response({"id": str(category_id), "name": data.get("name")}, request.headers.get('Accept', 'application/json')), 201
