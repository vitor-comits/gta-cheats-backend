# GTA Cheats Backend 🎮

Backend em Python / Flask estruturado para fornecer uma API REST com códigos e trapaças da franquia Grand Theft Auto.

## 🚀 Tecnologias

- **Python 3**
- **Flask**
- **Flask-CORS**
- **Python-dotenv**
- **Pytest**

## 📁 Estrutura do Projeto

```
gta-cheats-backend/
├── app/
│   ├── __init__.py        # Fábrica da aplicação Flask (Application Factory)
│   └── routes/
│       ├── __init__.py
│       ├── health.py      # Health check (/api/health)
│       └── cheats.py      # Rotas de cheats (/api/cheats)
├── tests/
│   └── test_api.py        # Testes automatizados com Pytest
├── .env.example           # Exemplo de variáveis de ambiente
├── .env                   # Variáveis de ambiente locais
├── .gitignore             # Arquivos ignorados pelo Git
├── config.py              # Classes de configuração (Dev, Prod, Test)
├── requirements.txt       # Dependências do projeto
└── run.py                 # Ponto de entrada da aplicação
```

## 🛠️ Instalação e Execução

### 1. Criar e ativar o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Copie o `.env.example` para `.env` caso ainda não exista:

```bash
cp .env.example .env
```

### 4. Executar a aplicação

```bash
python3 run.py
```

A API estará disponível em: `http://localhost:5000`

## 🧪 Executar Testes

```bash
pytest
```

## 📡 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/health` | Status de saúde da aplicação |
| `GET` | `/api/cheats` | Lista todos os cheats (suporta filtros `?game=gta-sa` e `?category=vehicles`) |
| `GET` | `/api/cheats/<id>` | Detalhes de um cheat específico por ID |