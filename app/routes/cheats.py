from flask import Blueprint, jsonify, request
from bson import ObjectId
from bson.errors import InvalidId
from app.db import get_cheats_collection

cheats_bp = Blueprint("cheats", __name__)


def format_cheat(doc: dict) -> dict:
    """Converte ObjectId para string e formata o documento para JSON."""
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


@cheats_bp.route("/cheats", methods=["GET"])
def get_cheats():
    """Retorna lista de cheats da coleção 'cheats' do banco 'gta' com filtros opcionais."""
    collection = get_cheats_collection()
    if collection is None:
        return jsonify({"error": "Banco de dados não disponível"}), 503

    game_filter = request.args.get("game")
    category_filter = request.args.get("category")

    query = {}
    if game_filter:
        query["game"] = {"$regex": f"^{game_filter}$", "$options": "i"}
    if category_filter:
        query["category"] = {"$regex": f"^{category_filter}$", "$options": "i"}

    cursor = collection.find(query)
    cheats = [format_cheat(doc) for doc in cursor]

    return jsonify({
        "count": len(cheats),
        "cheats": cheats
    }), 200


@cheats_bp.route("/cheats", methods=["POST"])
def create_cheat():
    """Cadastra um novo cheat na coleção 'cheats'."""
    collection = get_cheats_collection()
    if collection is None:
        return jsonify({"error": "Banco de dados não disponível"}), 503

    data = request.get_json()
    if not data:
        return jsonify({"error": "Corpo da requisição deve ser um JSON válido"}), 400

    required_fields = ["game", "title"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({"error": f"Campos obrigatórios ausentes: {', '.join(missing)}"}), 400

    new_cheat = {
        "game": data.get("game"),
        "game_name": data.get("game_name", data.get("game")),
        "title": data.get("title"),
        "code_pc": data.get("code_pc"),
        "code_playstation": data.get("code_playstation"),
        "code_xbox": data.get("code_xbox"),
        "code_phone": data.get("code_phone"),
        "category": data.get("category", "general")
    }

    result = collection.insert_one(new_cheat)
    new_cheat["id"] = str(result.inserted_id)
    if "_id" in new_cheat:
        new_cheat.pop("_id")

    return jsonify(new_cheat), 201


@cheats_bp.route("/cheats/<string:cheat_id>", methods=["DELETE"])
def delete_cheat(cheat_id: str):
    """Exclui um cheat da coleção pelo ID."""
    collection = get_cheats_collection()
    if collection is None:
        return jsonify({"error": "Banco de dados não disponível"}), 503

    deleted_count = 0
    try:
        res = collection.delete_one({"_id": ObjectId(cheat_id)})
        deleted_count = res.deleted_count
    except InvalidId:
        pass

    if deleted_count == 0 and cheat_id.isdigit():
        res = collection.delete_one({"custom_id": int(cheat_id)})
        deleted_count = res.deleted_count

    if deleted_count == 0:
        return jsonify({"error": "Cheat não encontrado"}), 404

    return jsonify({"message": "Cheat excluído com sucesso"}), 200