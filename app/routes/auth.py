import os
from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__)


def get_expected_credentials():
    """Retorna as credenciais e token configurados para o administrador."""
    expected_username = os.getenv("ADMIN_USERNAME", "admin").strip()
    expected_password = os.getenv("ADMIN_PASSWORD", "admin123").strip()
    expected_token = os.getenv("ADMIN_TOKEN", "gta-admin-secret-token-12345").strip()
    return expected_username, expected_password, expected_token


def is_admin_token_valid(token: str | None) -> bool:
    """Verifica se um token recebido confere com o token ou senha de admin."""
    if not token:
        return False
    _, expected_password, expected_token = get_expected_credentials()
    return token in (expected_token, expected_password)


@auth_bp.route("/auth/login", methods=["POST"])
def admin_login():
    """Autentica o administrador e retorna o token de acesso."""
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()

    expected_username, expected_password, expected_token = get_expected_credentials()

    if not username or not password:
        return jsonify({"error": "Usuário e senha são obrigatórios."}), 400

    if username == expected_username and password == expected_password:
        return jsonify({
            "success": True,
            "message": "Autenticação realizada com sucesso.",
            "token": expected_token,
            "username": expected_username
        }), 200

    return jsonify({"error": "Usuário ou senha inválidos."}), 401


@auth_bp.route("/auth/verify", methods=["GET"])
def admin_verify():
    """Verifica se a sessão/token do administrador continua válida."""
    token = None
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()

    if not token:
        token = request.headers.get("x-admin-key", "").strip()

    if is_admin_token_valid(token):
        expected_username, _, _ = get_expected_credentials()
        return jsonify({
            "authenticated": True,
            "username": expected_username
        }), 200

    return jsonify({"authenticated": False, "error": "Token inválido ou sessão expirada."}), 401
