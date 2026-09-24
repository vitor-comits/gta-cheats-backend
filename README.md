# GTA Cheats Backend 🎮

Backend em Python / Flask estruturado para fornecer uma API REST com códigos e trapaças da franquia Grand Theft Auto, integrado ao **MongoDB Atlas** e documentado interativamente via **Swagger UI**.

## 🚀 Tecnologias

- **Python 3**
- **Flask**
- **PyMongo** (MongoDB Atlas)
- **Flask-CORS**
- **Flask-Swagger-UI** (OpenAPI 3.0)
- **Python-dotenv**

## 📁 Estrutura do Projeto

```
gta-cheats-backend/
├── app/
│   ├── __init__.py        # Fábrica da aplicação Flask e registro do Swagger UI
│   ├── db.py              # Gerenciador de conexão com o MongoDB Atlas (banco gta)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── health.py      # Health check com status do MongoDB (/api/health)
│   │   └── cheats.py      # Rotas CRUD de cheats no MongoDB (/api/cheats)
│   └── static/
│       └── swagger.json   # Especificação OpenAPI 3.0
├── .env.example           # Exemplo de variáveis de ambiente
├── .env                   # Variáveis de ambiente locais (credenciais MongoDB Atlas)
├── .gitignore             # Arquivos ignorados pelo Git
├── config.py              # Classes de configuração da aplicação
├── requirements.txt       # Dependências do projeto
└── run.py                 # Ponto de entrada da aplicação
```

## 🛠️ Instalação e Execução

### 1. Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

O arquivo `.env` contém as configurações de conexão:

```env
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000
HOST=0.0.0.0
MONGODB_URI="mongodb+srv://<usuario>:<senha>@cluster.mongodb.net"
MONGODB_DB_NAME="gta"
```

### 4. Executar a aplicação

```bash
python run.py
```

A API estará disponível em: `http://localhost:5000`

---

## 📖 Documentação Interativa (Swagger UI)

Acesse a interface interativa do Swagger para testar todas as rotas diretamente pelo navegador:

👉 **`http://localhost:5000/docs`**

A especificação OpenAPI 3.0 bruta pode ser consultada em: `http://localhost:5000/docs/swagger.json`

---

## 📡 Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/health` | Status de saúde da aplicação e conectividade com o MongoDB Atlas |
| `GET` | `/api/cheats` | Lista todos os cheats (suporta filtros `?game=gta-sa` e `?category=vehicles`) |
| `POST` | `/api/cheats` | Cadastra um novo cheat na coleção `cheats` do MongoDB |
| `GET` | `/api/cheats/<id>` | Busca um cheat por ID (`ObjectId` ou `custom_id`) |
| `DELETE` | `/api/cheats/<id>` | Remove um cheat por ID |