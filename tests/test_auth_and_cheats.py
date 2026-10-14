import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def test_admin_login_success(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "token" in data
    assert data["username"] == "admin"


def test_admin_login_invalid_password(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data


def test_admin_login_missing_fields(client):
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 400


def test_admin_verify_valid_token(client):
    login_res = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    token = login_res.get_json()["token"]

    verify_res = client.get(
        "/api/auth/verify",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert verify_res.status_code == 200
    assert verify_res.get_json()["authenticated"] is True


def test_admin_verify_invalid_token(client):
    verify_res = client.get(
        "/api/auth/verify",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert verify_res.status_code == 401
    assert verify_res.get_json()["authenticated"] is False


def test_cheats_mutation_requires_admin_auth(client):
    # POST sem autenticação deve retornar 401
    post_res = client.post(
        "/api/cheats",
        json={"game": "gta-v", "title": "Cheat Não Autorizado"},
    )
    assert post_res.status_code == 401

    # Login como admin
    login_res = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    token = login_res.get_json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # POST com autenticação deve ser permitido (201)
    create_res = client.post(
        "/api/cheats",
        json={
            "game": "gta-v",
            "game_name": "Grand Theft Auto V",
            "title": "Cheat Teste Automatizado",
            "code_pc": "TESTCODE",
            "category": "player",
        },
        headers=headers,
    )
    assert create_res.status_code == 201
    cheat_data = create_res.get_json()
    cheat_id = cheat_data["id"]

    # PUT sem autenticação deve retornar 401
    put_unauth = client.put(
        f"/api/cheats/{cheat_id}",
        json={"title": "Tentativa Não Autorizada"},
    )
    assert put_unauth.status_code == 401

    # PUT com autenticação deve ser permitido (200)
    put_res = client.put(
        f"/api/cheats/{cheat_id}",
        json={"title": "Cheat Teste Atualizado"},
        headers=headers,
    )
    assert put_res.status_code == 200
    assert put_res.get_json()["cheat"]["title"] == "Cheat Teste Atualizado"

    # DELETE sem autenticação deve retornar 401
    delete_unauth = client.delete(f"/api/cheats/{cheat_id}")
    assert delete_unauth.status_code == 401

    # DELETE com autenticação deve ser permitido (200)
    delete_res = client.delete(f"/api/cheats/{cheat_id}", headers=headers)
    assert delete_res.status_code == 200
