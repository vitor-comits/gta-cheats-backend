from flask import Blueprint, jsonify, current_app
from app.db import check_db_status

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Endpoint de checagem de saúde da API e conexão com o MongoDB Atlas."""
    db_connected = check_db_status()
    db_name = current_app.config.get("MONGODB_DB_NAME", "gta")

    return jsonify({
        "status": "ok",
        "service": "gta-cheats-backend",
        "version": "1.0.0",
        "database": "connected" if db_connected else "disconnected",
        "database_name": db_name
    }), 200
