import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from config import config_by_name, DevelopmentConfig
from app.db import init_db


def create_app(config_name: str | None = None) -> Flask:
    """Fábrica de aplicação Flask com MongoDB e Swagger UI."""
    app = Flask(__name__)

    # Determina a configuração baseada no argumento ou variável de ambiente
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    config_class = config_by_name.get(config_name, DevelopmentConfig)
    app.config.from_object(config_class)

    # Habilita CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Inicializa conexão com o MongoDB Atlas
    init_db(app)

    # Configuração da documentação Swagger UI
    SWAGGER_URL = "/docs"
    API_URL = "/docs/swagger.json"

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "GTA Cheats API",
            "layout": "BaseLayout",
            "deepLinking": True
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/docs/swagger.json")
    def serve_swagger_spec():
        """Serve o arquivo estático da especificação OpenAPI / Swagger, ocultando rotas de mutação na Vercel."""
        spec_path = os.path.join(app.root_path, "static", "swagger.json")
        is_vercel = os.getenv("VERCEL") == "1" or os.getenv("ENV") == "production" or os.getenv("FLASK_ENV") == "production"

        if is_vercel:
            import json
            with open(spec_path, "r", encoding="utf-8") as f:
                spec_data = json.load(f)

            # Remove POST /api/cheats e DELETE /api/cheats/{id} na Vercel/produção
            if "/api/cheats" in spec_data.get("paths", {}):
                spec_data["paths"]["/api/cheats"].pop("post", None)
            if "/api/cheats/{id}" in spec_data.get("paths", {}):
                spec_data["paths"]["/api/cheats/{id}"].pop("delete", None)

            return jsonify(spec_data)

        return send_from_directory(os.path.join(app.root_path, "static"), "swagger.json")

    # Registro de Blueprints da API
    from app.routes.health import health_bp
    from app.routes.cheats import cheats_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(cheats_bp, url_prefix="/api")

    # Tratamento global de erros JSON
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Recurso não encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Erro interno do servidor"}), 500

    return app
