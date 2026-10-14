import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuração base compartilhada."""
    SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-secret-key")
    JSON_SORT_KEYS = False
    MONGODB_URI = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "gta")
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "gta-admin-secret-token-12345")


class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Configuração para execução de testes automatizados."""
    DEBUG = False
    TESTING = True
    SECRET_KEY = "test-secret-key"


class ProductionConfig(Config):
    """Configuração para ambiente de produção."""
    DEBUG = False
    TESTING = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
