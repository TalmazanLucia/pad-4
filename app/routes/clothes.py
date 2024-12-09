from flask import Blueprint, request
import uuid
from app.helper import create_response
from app import session, cache

clothes_bp = Blueprint('clothes', __name__)

@clothes_bp.route('', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_clothes():
    filters = request.args
    query = "SELECT * FROM clothes"
    params = []
    conditions = []

    # Filtering conditions
    if 'category_id' in filters:
        try:
            conditions.append("category_id = ?")
            params.append(uuid.UUID(filters['category_id']))
        except ValueError:
            return create_response(
                {"error": "Invalid category_id UUID"},
                request.headers.get('Accept', 'application/json')
            ), 400

    if 'size' in filters:
        conditions.append("size = ?")
        params.append(filters['size'])

    if 'is_available' in filters:
        conditions.append("is_available = ?")
        params.append(filters['is_available'].lower() == 'true')

    # Apply conditions to query
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    # Add ALLOW FILTERING if necessary
    query += " ALLOW FILTERING"

    # Prepare the statement
    try:
        statement = session.prepare(query)
    except ValueError:
        return create_response(
            {"error": f"Invalid query syntax"},
            request.headers.get('Accept', 'application/json')
        ), 400

    # Execute the query and fetch all matching rows
    result = session.execute(statement, params)

    clothes = []
    for row in result:
        clothes.append({
            "id": str(row.id),
            "name": row.name,
            "size": row.size,
            "price": row.price,
            "stock": row.stock,
            "color": row.color,
            "brand": row.brand,
            "material": row.material,
            "description": row.description,
            "is_available": row.is_available,
            "category_id": str(row.category_id),
            "rating": row.rating,
        })

    response_data = {
        "clothes": clothes
    }

    return create_response(
        response_data,
        request.headers.get('Accept', 'application/json')
    ), 200


@clothes_bp.route('', methods=['POST'])
def add_clothes():
    data = request.json

    # Validation
    if not data.get("category_id") or not data.get("name"):
        return create_response({"error": "Category ID and name are required"}, request.headers.get('Accept', 'application/json')), 400

    query = """
        INSERT INTO clothes (id, name, size, price, stock, color, brand, material, description, is_available, category_id, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    clothes_id = uuid.uuid4()
    session.execute(
        query,
        (
            clothes_id,
            data.get("name"),
            data.get("size"),
            data.get("price"),
            data.get("stock"),
            data.get("color"),
            data.get("brand"),
            data.get("material"),
            data.get("description"),
            data.get("is_available", True),
            uuid.UUID(data.get("category_id")),
            data.get("rating", 0.0),
        )
    )

    # Clear cache for clothes since new data is added
    cache.clear()

    return create_response({"id": str(clothes_id)}, request.headers.get('Accept', 'application/json')), 201

@clothes_bp.route('/<uuid:clothes_id>', methods=['GET'])
@cache.cached(timeout=300, key_prefix=lambda: f"clothes_{request.view_args['clothes_id']}")
def get_single_clothes(clothes_id):
    query = "SELECT * FROM clothes WHERE id = %s;"
    row = session.execute(query, (clothes_id,)).one_or_none()

    if not row:
        return create_response({"error": "Clothes item not found"}, request.headers.get('Accept', 'application/json')), 404

    clothes = {
        "id": str(row.id),
        "name": row.name,
        "size": row.size,
        "price": row.price,
        "stock": row.stock,
        "color": row.color,
        "brand": row.brand,
        "material": row.material,
        "description": row.description,
        "is_available": row.is_available,
        "category_id": str(row.category_id),
        "rating": row.rating,
    }
    return create_response(clothes, request.headers.get('Accept', 'application/json')), 200
