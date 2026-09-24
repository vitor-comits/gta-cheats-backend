from flask import Blueprint, jsonify, request

cheats_bp = Blueprint("cheats", __name__)

@cheats_bp.route("/cheats", methods=["GET"])
def get_cheats():
    """Retorna lista de cheats com suporte a filtros opcionais por jogo e categoria."""
    game_filter = request.args.get("game")
    category_filter = request.args.get("category")

    if game_filter:
        
            // TODO
            
            //
        

    if category_filter:
        
            // TODO

            //
        

    return jsonify({
        "count": len(filtered_cheats),
        "cheats": filtered_cheats
    }), 200