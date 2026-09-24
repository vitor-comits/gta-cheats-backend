from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Endpoint de checagem de saúde da API."""
    return jsonify({
        "status": "ok",
        "service": "gta-cheats-backend",
        "version": "1.0.0"
    }), 200

