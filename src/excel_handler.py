"""
Módulo para manipulação de arquivos Excel
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime


class ExcelHandler:
    """Classe para manipular arquivos Excel"""

    def __init__(self, file_path: Path):
        """
        Inicializa o manipulador de Excel

        Args:
            file_path: Caminho para o arquivo Excel
        """
        self.file_path = file_path
        self.df = None
        self.sheet_names = []

    def load_excel(self, sheet_name: Optional[str] = None) -> bool:
        """
        Carrega dados do arquivo Excel

        Args:
            sheet_name: Nome da planilha (opcional, usa a primeira por padrão)

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            if not self.file_path.exists():
                print(f"✗ Arquivo não encontrado: {self.file_path}")
                return False

            # Lê nomes das planilhas
            excel_file = pd.ExcelFile(self.file_path)
            self.sheet_names = excel_file.sheet_names

            # Carrega a planilha especificada ou a primeira
            if sheet_name:
                if sheet_name not in self.sheet_names:
                    print(f"✗ Planilha '{sheet_name}' não encontrada")
                    return False
                self.df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            else:
                self.df = pd.read_excel(self.file_path, sheet_name=0)

            print(f"✓ Excel carregado: {len(self.df)} linhas, {len(self.df.columns)} colunas")
            print(f"  Planilhas disponíveis: {', '.join(self.sheet_names)}")
            return True

        except Exception as e:
            print(f"✗ Erro ao carregar Excel: {e}")
            return False

    def get_dataframe(self) -> Optional[pd.DataFrame]:
        """
        Retorna o DataFrame atual

        Returns:
            DataFrame com os dados ou None
        """
        return self.df

    def get_column_names(self) -> List[str]:
        """
        Retorna nomes das colunas

        Returns:
            Lista com nomes das colunas
        """
        return list(self.df.columns) if self.df is not None else []

    def get_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre os dados

        Returns:
            Dicionário com informações
        """
        if self.df is None:
            return {}

        return {
            "total_linhas": len(self.df),
            "total_colunas": len(self.df.columns),
            "colunas": list(self.df.columns),
            "tipos_dados": self.df.dtypes.to_dict(),
            "valores_nulos": self.df.isnull().sum().to_dict(),
            "planilhas": self.sheet_names,
        }

    def show_preview(self, n_rows: int = 10) -> None:
        """
        Exibe preview dos dados

        Args:
            n_rows: Número de linhas a exibir
        """
        if self.df is None:
            print("✗ Nenhum dado carregado")
            return

        print("\n" + "=" * 80)
        print(f"PREVIEW DOS DADOS (primeiras {n_rows} linhas)")
        print("=" * 80)
        print(self.df.head(n_rows))
        print("=" * 80 + "\n")

    def clean_data(self) -> bool:
        """
        Realiza limpeza básica dos dados

        Returns:
            True se sucesso, False caso contrário
        """
        if self.df is None:
            print("✗ Nenhum dado carregado")
            return False

        try:
            initial_rows = len(self.df)

            # Remove linhas completamente vazias
            self.df = self.df.dropna(how="all")

            # Remove colunas completamente vazias
            self.df = self.df.dropna(axis=1, how="all")

            # Remove espaços em branco extras
            for col in self.df.select_dtypes(include=["object"]).columns:
                self.df[col] = self.df[col].str.strip() if self.df[col].dtype == "object" else self.df[col]

            # Reseta o índice
            self.df = self.df.reset_index(drop=True)

            rows_removed = initial_rows - len(self.df)
            print(f"✓ Limpeza concluída: {rows_removed} linha(s) vazias removidas")
            return True

        except Exception as e:
            print(f"✗ Erro ao limpar dados: {e}")
            return False

    def filter_data(self, column: str, value: Any) -> Optional[pd.DataFrame]:
        """
        Filtra dados por coluna e valor

        Args:
            column: Nome da coluna
            value: Valor a filtrar

        Returns:
            DataFrame filtrado ou None
        """
        if self.df is None:
            print("✗ Nenhum dado carregado")
            return None

        try:
            if column not in self.df.columns:
                print(f"✗ Coluna '{column}' não encontrada")
                return None

            filtered_df = self.df[self.df[column] == value]
            print(f"✓ Filtro aplicado: {len(filtered_df)} registros encontrados")
            return filtered_df

        except Exception as e:
            print(f"✗ Erro ao filtrar dados: {e}")
            return None

    def get_statistics(self) -> Optional[Dict[str, Any]]:
        """
        Retorna estatísticas descritivas dos dados numéricos

        Returns:
            Dicionário com estatísticas
        """
        if self.df is None:
            print("✗ Nenhum dado carregado")
            return None

        try:
            # Estatísticas para colunas numéricas
            numeric_stats = self.df.describe().to_dict()

            # Contagem de valores únicos para colunas categóricas
            categorical_stats = {}
            for col in self.df.select_dtypes(include=["object"]).columns:
                categorical_stats[col] = {
                    "valores_unicos": self.df[col].nunique(),
                    "mais_comum": (self.df[col].mode()[0] if not self.df[col].mode().empty else None),
                }

            return {
                "estatisticas_numericas": numeric_stats,
                "estatisticas_categoricas": categorical_stats,
            }

        except Exception as e:
            print(f"✗ Erro ao calcular estatísticas: {e}")
            return None

    def export_to_excel(
        self,
        output_path: Path,
        df: Optional[pd.DataFrame] = None,
        sheet_name: str = "Dados",
    ) -> bool:
        """
        Exporta dados para arquivo Excel

        Args:
            output_path: Caminho do arquivo de saída
            df: DataFrame a exportar (usa self.df se None)
            sheet_name: Nome da planilha

        Returns:
            True se sucesso, False caso contrário
        """
        try:
            data_to_export = df if df is not None else self.df

            if data_to_export is None:
                print("✗ Nenhum dado para exportar")
                return False

            # Cria diretório se não existir
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Exporta para Excel
            data_to_export.to_excel(output_path, sheet_name=sheet_name, index=False)
            print(f"✓ Dados exportados para: {output_path}")
            print(f"  {len(data_to_export)} linhas, {len(data_to_export.columns)} colunas")
            return True

        except Exception as e:
            print(f"✗ Erro ao exportar Excel: {e}")
            return False

    def add_column(self, column_name: str, values: List[Any]) -> bool:
        """
        Adiciona uma nova coluna ao DataFrame

        Args:
            column_name: Nome da nova coluna
            values: Lista com os valores

        Returns:
            True se sucesso, False caso contrário
        """
        if self.df is None:
            print("✗ Nenhum dado carregado")
            return False

        try:
            if len(values) != len(self.df):
                print(f"✗ Número de valores ({len(values)}) diferente do número de linhas ({len(self.df)})")
                return False

            self.df[column_name] = values
            print(f"✓ Coluna '{column_name}' adicionada")
            return True

        except Exception as e:
            print(f"✗ Erro ao adicionar coluna: {e}")
            return False

    def remove_column(self, column_name: str) -> bool:
        """
        Remove uma coluna do DataFrame

        Args:
            column_name: Nome da coluna a remover

        Returns:
            True se sucesso, False caso contrário
        """
        if self.df is None:
            print("✗ Nenhum dado carregado")
            return False

        try:
            if column_name not in self.df.columns:
                print(f"✗ Coluna '{column_name}' não encontrada")
                return False

            self.df = self.df.drop(columns=[column_name])
            print(f"✓ Coluna '{column_name}' removida")
            return True

        except Exception as e:
            print(f"✗ Erro ao remover coluna: {e}")
            return False
