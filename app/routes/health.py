from flask import Blueprint, jsonify, current_app

health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def health_check():
    node_id = current_app.config['NODE_ID']
    return jsonify({
        "status": "healthy",
        "node_id": node_id
    }), 200
