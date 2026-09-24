import pytest
from app import create_app


@pytest.fixture
def client():
    """Fixture que cria cliente de testes com configuração de testing."""
    app = create_app("testing")
    with app.test_client() as test_client:
        yield test_client


def test_health_check(client):
    """Testa se o endpoint de saúde responde 200 com status 'ok'."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "gta-cheats-backend"


def test_get_all_cheats(client):
    """Testa listagem completa de cheats."""
    response = client.get("/api/cheats")
    assert response.status_code == 200
    data = response.get_json()
    assert "cheats" in data
    assert data["count"] == len(data["cheats"])
    assert data["count"] > 0


def test_filter_cheats_by_game(client):
    """Testa filtro de cheats por jogo (ex: gta-sa)."""
    response = client.get("/api/cheats?game=gta-sa")
    assert response.status_code == 200
    data = response.get_json()
    for cheat in data["cheats"]:
        assert cheat["game"] == "gta-sa"


def test_get_cheat_by_id_found(client):
    """Testa busca de cheat por ID existente."""
    response = client.get("/api/cheats/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert "title" in data


def test_get_cheat_by_id_not_found(client):
    """Testa busca de cheat com ID inexistente."""
    response = client.get("/api/cheats/9999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_route_not_found(client):
    """Testa retorno 404 em rota inexistente."""
    response = client.get("/api/rota-inexistente")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

