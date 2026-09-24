import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config_by_name, DevelopmentConfig
from app.routes.health import health_bp
from app.routes.cheats import cheats_bp

def create_app(config_name: str | None = None) -> Flask:
    """Fábrica de aplicação Flask."""
    app = Flask(__name__)
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")
    config_class = config_by_name.get(config_name, DevelopmentConfig)
    app.config.from_object(config_class)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(cheats_bp, url_prefix="/api")

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Recurso não encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Erro interno do servidor"}), 500

    return app

