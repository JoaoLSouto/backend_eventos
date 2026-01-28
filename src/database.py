"""
Módulo para gerenciamento do banco de dados SQLite
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime


class Database:
    """Classe para gerenciar operações com banco de dados SQLite"""

    def __init__(self, db_path: Path):
        """
        Inicializa a conexão com o banco de dados

        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        self.connection = None
        self.connect()

    def connect(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            print(f"✓ Conectado ao banco de dados: {self.db_path.name}")
        except sqlite3.Error as e:
            print(f"✗ Erro ao conectar ao banco: {e}")
            raise

    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
            print("✓ Conexão com banco de dados fechada")

    def create_table_from_dataframe(
        self, df: pd.DataFrame, table_name: str, if_exists: str = "replace"
    ) -> bool:
        """
        Cria uma tabela a partir de um DataFrame pandas

        Args:
            df: DataFrame com os dados
            table_name: Nome da tabela a ser criada
            if_exists: 'fail', 'replace' ou 'append'

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            df.to_sql(table_name, self.connection, if_exists=if_exists, index=False)
            print(f"✓ Tabela '{table_name}' criada com {len(df)} registros")
            return True
        except Exception as e:
            print(f"✗ Erro ao criar tabela: {e}")
            return False

    def execute_query(self, query: str, params: tuple = ()) -> Optional[List[Dict]]:
        """
        Executa uma query SQL e retorna os resultados

        Args:
            query: Query SQL a ser executada
            params: Parâmetros para a query (opcional)

        Returns:
            Lista de dicionários com os resultados ou None em caso de erro
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)

            # Se for um SELECT, retorna os resultados
            if query.strip().upper().startswith("SELECT"):
                columns = [description[0] for description in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return results
            else:
                # Para INSERT, UPDATE, DELETE
                self.connection.commit()
                print(f"✓ Query executada: {cursor.rowcount} linha(s) afetada(s)")
                return None
        except sqlite3.Error as e:
            print(f"✗ Erro ao executar query: {e}")
            return None

    def get_table_names(self) -> List[str]:
        """
        Retorna lista com nomes de todas as tabelas do banco

        Returns:
            Lista com nomes das tabelas
        """
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        result = self.execute_query(query)
        return [row["name"] for row in result] if result else []

    def get_table_info(self, table_name: str) -> Optional[List[Dict]]:
        """
        Retorna informações sobre as colunas de uma tabela

        Args:
            table_name: Nome da tabela

        Returns:
            Lista com informações das colunas
        """
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)

    def get_table_as_dataframe(
        self, table_name: str, where_clause: str = ""
    ) -> Optional[pd.DataFrame]:
        """
        Retorna uma tabela como DataFrame pandas

        Args:
            table_name: Nome da tabela
            where_clause: Cláusula WHERE opcional (ex: "WHERE idade > 18")

        Returns:
            DataFrame com os dados da tabela
        """
        try:
            query = f"SELECT * FROM {table_name} {where_clause}"
            df = pd.read_sql_query(query, self.connection)
            return df
        except Exception as e:
            print(f"✗ Erro ao ler tabela: {e}")
            return None

    def insert_record(self, table_name: str, data: Dict[str, Any]) -> bool:
        """
        Insere um registro na tabela

        Args:
            table_name: Nome da tabela
            data: Dicionário com os dados a inserir

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            cursor = self.connection.cursor()
            cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            print(f"✓ Registro inserido com sucesso")
            return True
        except sqlite3.Error as e:
            print(f"✗ Erro ao inserir registro: {e}")
            return False

    def update_record(
        self,
        table_name: str,
        data: Dict[str, Any],
        where_clause: str,
        where_params: tuple = (),
    ) -> bool:
        """
        Atualiza registros na tabela

        Args:
            table_name: Nome da tabela
            data: Dicionário com os dados a atualizar
            where_clause: Cláusula WHERE (ex: "id = ?")
            where_params: Parâmetros para a cláusula WHERE

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

            params = tuple(data.values()) + where_params
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            print(f"✓ {cursor.rowcount} registro(s) atualizado(s)")
            return True
        except sqlite3.Error as e:
            print(f"✗ Erro ao atualizar registro: {e}")
            return False

    def delete_record(
        self, table_name: str, where_clause: str, where_params: tuple = ()
    ) -> bool:
        """
        Deleta registros da tabela

        Args:
            table_name: Nome da tabela
            where_clause: Cláusula WHERE (ex: "id = ?")
            where_params: Parâmetros para a cláusula WHERE

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            query = f"DELETE FROM {table_name} WHERE {where_clause}"
            cursor = self.connection.cursor()
            cursor.execute(query, where_params)
            self.connection.commit()
            print(f"✓ {cursor.rowcount} registro(s) deletado(s)")
            return True
        except sqlite3.Error as e:
            print(f"✗ Erro ao deletar registro: {e}")
            return False

    def get_table_statistics(self, table_name: str) -> Dict[str, Any]:
        """
        Retorna estatísticas básicas sobre a tabela

        Args:
            table_name: Nome da tabela

        Returns:
            Dicionário com estatísticas
        """
        try:
            # Total de registros
            query = f"SELECT COUNT(*) as total FROM {table_name}"
            result = self.execute_query(query)
            total = result[0]["total"] if result else 0

            # Informações das colunas
            columns_info = self.get_table_info(table_name)
            num_columns = len(columns_info) if columns_info else 0

            return {
                "total_registros": total,
                "total_colunas": num_columns,
                "colunas": (
                    [col["name"] for col in columns_info] if columns_info else []
                ),
            }
        except Exception as e:
            print(f"✗ Erro ao obter estatísticas: {e}")
            return {}
