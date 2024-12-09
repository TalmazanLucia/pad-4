from flask import Blueprint, jsonify, current_app

status_bp = Blueprint('status', __name__)

@status_bp.route('/', methods=['GET'])
def node_status():
    node_id = current_app.config['NODE_ID']
    return jsonify({
        "node_id": node_id,
        "status": "active"
    }), 200
