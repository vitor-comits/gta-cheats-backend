import logging
from typing import Optional
from flask import Flask
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, PyMongoError

logger = logging.getLogger(__name__)

_mongo_client: Optional[MongoClient] = None
_db_instance: Optional[Database] = None


def get_client() -> Optional[MongoClient]:
    """Retorna o cliente MongoClient atual."""
    return _mongo_client


def get_db() -> Optional[Database]:
    """Retorna a instância do banco de dados configurado (gta)."""
    return _db_instance


def get_cheats_collection() -> Optional[Collection]:
    """Retorna a coleção 'cheats' do banco 'gta'."""
    db = get_db()
    if db is not None:
        return db["cheats"]
    return None


def check_db_status() -> bool:
    """Verifica se a conexão com o MongoDB está ativa via comando ping."""
    if _mongo_client is None:
        return False
    try:
        _mongo_client.admin.command("ping")
        return True
    except (ConnectionFailure, PyMongoError):
        return False


def seed_initial_cheats(collection: Collection) -> None:
    """Insere cheats iniciais se a coleção estiver vazia."""
    try:
        if collection.count_documents({}) == 0:
            initial_data = [
                {
                    "custom_id": 1,
                    "game": "gta-sa",
                    "game_name": "Grand Theft Auto: San Andreas",
                    "title": "Saúde, Colete e $250.000",
                    "code_pc": "HESOYAM",
                    "code_playstation": "R1, R2, L1, X, Esquerda, Baixo, Direita, Cima, Esquerda, Baixo, Direita, Cima",
                    "code_xbox": "RT, RB, LT, A, Esquerda, Baixo, Direita, Cima, Esquerda, Baixo, Direita, Cima",
                    "category": "player"
                },
                {
                    "custom_id": 2,
                    "game": "gta-sa",
                    "game_name": "Grand Theft Auto: San Andreas",
                    "title": "Jetpack (Mochila a jato)",
                    "code_pc": "ROCKETMAN",
                    "code_playstation": "L1, L2, R1, R2, Cima, Baixo, Esquerda, Direita, L1, L2, R1, R2, Cima, Baixo, Esquerda, Direita",
                    "code_xbox": "LT, LB, RT, RB, Cima, Baixo, Esquerda, Direita, LT, LB, RT, RB, Cima, Baixo, Esquerda, Direita",
                    "category": "vehicles"
                },
                {
                    "custom_id": 3,
                    "game": "gta-v",
                    "game_name": "Grand Theft Auto V",
                    "title": "Invencibilidade (5 minutos)",
                    "code_pc": "PAINKILLER",
                    "code_playstation": "Direita, X, Direita, Esquerda, Direita, R1, Direita, Esquerda, X, Triângulo",
                    "code_xbox": "Direita, A, Direita, Esquerda, Direita, RB, Direita, Esquerda, A, Y",
                    "category": "player"
                },
                {
                    "custom_id": 4,
                    "game": "gta-v",
                    "game_name": "Grand Theft Auto V",
                    "title": "Gerar Helicóptero Buzzard",
                    "code_pc": "BUZZOFF",
                    "code_playstation": "Círculo, Círculo, L1, Círculo, Círculo, Círculo, L1, L2, R1, Triângulo, Círculo, Triângulo",
                    "code_xbox": "B, B, LB, B, B, B, LB, LT, RB, Y, B, Y",
                    "category": "vehicles"
                }
            ]
            collection.insert_many(initial_data)
            logger.info("Seed inicial inserido com sucesso na coleção 'cheats'.")
    except Exception as e:
        logger.warning(f"Não foi possível efetuar o seed inicial: {e}")


def init_db(app: Flask) -> None:
    """Inicializa a conexão com o MongoDB Atlas."""
    global _mongo_client, _db_instance

    uri = app.config.get("MONGODB_URI")
    db_name = app.config.get("MONGODB_DB_NAME", "gta")

    if not uri:
        logger.warning("MONGODB_URI não foi configurada. Executando sem banco de dados.")
        return

    try:
        _mongo_client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Testa a conectividade
        _mongo_client.admin.command("ping")
        _db_instance = _mongo_client[db_name]
        logger.info(f"Conectado ao MongoDB Atlas com sucesso! Banco: '{db_name}'")

        # Verifica e executa seed inicial se necessário
        cheats_col = _db_instance["cheats"]
        seed_initial_cheats(cheats_col)

    except Exception as e:
        logger.error(f"Erro ao conectar com MongoDB Atlas: {e}")
        # Mantém a aplicação rodando mesmo se a conexão falhar
        _db_instance = None

