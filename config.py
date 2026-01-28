"""
Configurações do projeto
"""

import os
from pathlib import Path

# Diretórios do projeto
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SRC_DIR = BASE_DIR / "src"

# Configurações do banco de dados
DATABASE_NAME = "eventos.db"
DATABASE_PATH = DATA_DIR / DATABASE_NAME

# Configurações de Excel
EXCEL_FILE_PATH = BASE_DIR / "Vip Funn 01.06.xlsx"

# Criar diretórios se não existirem
DATA_DIR.mkdir(exist_ok=True)
