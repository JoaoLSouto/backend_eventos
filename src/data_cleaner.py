"""
Módulo para tratamento e limpeza avançada de dados
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re


class DataCleaner:
    """Classe para realizar tratamento e limpeza avançada de dados"""

    def __init__(self, df: pd.DataFrame):
        """
        Inicializa o limpador de dados

        Args:
            df: DataFrame a ser limpo
        """
        self.df = df.copy()
        self.original_df = df.copy()
        self.cleaning_log = []

    def remove_duplicates(self, subset: Optional[List[str]] = None, keep: str = "first") -> pd.DataFrame:
        """
        Remove registros duplicados

        Args:
            subset: Lista de colunas para considerar na verificação
            keep: 'first', 'last' ou False

        Returns:
            DataFrame sem duplicados
        """
        before = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        after = len(self.df)
        removed = before - after

        self.cleaning_log.append(f"Duplicados removidos: {removed}")
        print(f"✓ {removed} registro(s) duplicado(s) removido(s)")
        return self.df

    def handle_missing_values(
        self, strategy: str = "drop", fill_value: Any = None, columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Trata valores ausentes (NaN)

        Args:
            strategy: 'drop', 'fill', 'forward', 'backward', 'mean', 'median'
            fill_value: Valor para preencher (quando strategy='fill')
            columns: Lista de colunas específicas (None = todas)

        Returns:
            DataFrame tratado
        """
        cols = columns if columns else self.df.columns

        if strategy == "drop":
            before = len(self.df)
            self.df = self.df.dropna(subset=cols if columns else None)
            removed = before - len(self.df)
            self.cleaning_log.append(f"Linhas com NaN removidas: {removed}")
            print(f"✓ {removed} linha(s) com valores ausentes removida(s)")

        elif strategy == "fill":
            for col in cols:
                if col in self.df.columns:
                    self.df[col].fillna(fill_value, inplace=True)
            self.cleaning_log.append(f"Valores ausentes preenchidos com: {fill_value}")
            print(f"✓ Valores ausentes preenchidos")

        elif strategy == "forward":
            self.df[cols] = self.df[cols].fillna(method="ffill")
            self.cleaning_log.append("Forward fill aplicado")
            print(f"✓ Forward fill aplicado")

        elif strategy == "backward":
            self.df[cols] = self.df[cols].fillna(method="bfill")
            self.cleaning_log.append("Backward fill aplicado")
            print(f"✓ Backward fill aplicado")

        elif strategy == "mean":
            for col in cols:
                if col in self.df.columns and pd.api.types.is_numeric_dtype(self.df[col]):
                    mean_val = self.df[col].mean()
                    self.df[col].fillna(mean_val, inplace=True)
            self.cleaning_log.append("Valores ausentes preenchidos com média")
            print(f"✓ Valores ausentes preenchidos com média")

        elif strategy == "median":
            for col in cols:
                if col in self.df.columns and pd.api.types.is_numeric_dtype(self.df[col]):
                    median_val = self.df[col].median()
                    self.df[col].fillna(median_val, inplace=True)
            self.cleaning_log.append("Valores ausentes preenchidos com mediana")
            print(f"✓ Valores ausentes preenchidos com mediana")

        return self.df

    def standardize_text(self, columns: Optional[List[str]] = None, operation: str = "lower") -> pd.DataFrame:
        """
        Padroniza texto (maiúsculas, minúsculas, capitalizar)

        Args:
            columns: Lista de colunas (None = todas as de texto)
            operation: 'lower', 'upper', 'title', 'strip'

        Returns:
            DataFrame com texto padronizado
        """
        text_cols = columns if columns else self.df.select_dtypes(include=["object"]).columns

        for col in text_cols:
            if col in self.df.columns:
                if operation == "lower":
                    self.df[col] = self.df[col].str.lower()
                elif operation == "upper":
                    self.df[col] = self.df[col].str.upper()
                elif operation == "title":
                    self.df[col] = self.df[col].str.title()
                elif operation == "strip":
                    self.df[col] = self.df[col].str.strip()

        self.cleaning_log.append(f"Texto padronizado: {operation}")
        print(f"✓ Texto padronizado ({operation})")
        return self.df

    def remove_special_characters(self, columns: List[str], keep_spaces: bool = True) -> pd.DataFrame:
        """
        Remove caracteres especiais de colunas de texto

        Args:
            columns: Lista de colunas
            keep_spaces: Se True, mantém espaços

        Returns:
            DataFrame limpo
        """
        pattern = r"[^a-zA-Z0-9\s]" if keep_spaces else r"[^a-zA-Z0-9]"

        for col in columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].str.replace(pattern, "", regex=True)

        self.cleaning_log.append(f"Caracteres especiais removidos de: {', '.join(columns)}")
        print(f"✓ Caracteres especiais removidos")
        return self.df

    def convert_data_types(self, type_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Converte tipos de dados das colunas

        Args:
            type_mapping: Dicionário {coluna: tipo} ex: {'idade': 'int', 'valor': 'float'}

        Returns:
            DataFrame com tipos convertidos
        """
        for col, dtype in type_mapping.items():
            if col in self.df.columns:
                try:
                    if dtype == "int":
                        self.df[col] = pd.to_numeric(self.df[col], errors="coerce").fillna(0).astype(int)
                    elif dtype == "float":
                        self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
                    elif dtype == "datetime":
                        self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
                    elif dtype == "str":
                        self.df[col] = self.df[col].astype(str)

                    self.cleaning_log.append(f"Coluna '{col}' convertida para {dtype}")
                    print(f"✓ Coluna '{col}' convertida para {dtype}")
                except Exception as e:
                    print(f"✗ Erro ao converter '{col}': {e}")

        return self.df

    def remove_outliers(self, columns: List[str], method: str = "iqr", threshold: float = 1.5) -> pd.DataFrame:
        """
        Remove outliers de colunas numéricas

        Args:
            columns: Lista de colunas numéricas
            method: 'iqr' (Interquartile Range) ou 'zscore'
            threshold: Limite para considerar outlier (1.5 para IQR, 3 para zscore)

        Returns:
            DataFrame sem outliers
        """
        before = len(self.df)

        for col in columns:
            if col in self.df.columns and pd.api.types.is_numeric_dtype(self.df[col]):
                if method == "iqr":
                    Q1 = self.df[col].quantile(0.25)
                    Q3 = self.df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - threshold * IQR
                    upper = Q3 + threshold * IQR
                    self.df = self.df[(self.df[col] >= lower) & (self.df[col] <= upper)]

                elif method == "zscore":
                    z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                    self.df = self.df[z_scores < threshold]

        after = len(self.df)
        removed = before - after
        self.cleaning_log.append(f"Outliers removidos: {removed} ({method})")
        print(f"✓ {removed} outlier(s) removido(s) usando método {method}")
        return self.df

    def normalize_column(self, column: str, method: str = "minmax") -> pd.DataFrame:
        """
        Normaliza valores de uma coluna numérica

        Args:
            column: Nome da coluna
            method: 'minmax' (0-1) ou 'zscore' (média=0, desvio=1)

        Returns:
            DataFrame com coluna normalizada
        """
        if column not in self.df.columns:
            print(f"✗ Coluna '{column}' não encontrada")
            return self.df

        if method == "minmax":
            min_val = self.df[column].min()
            max_val = self.df[column].max()
            self.df[column] = (self.df[column] - min_val) / (max_val - min_val)
            self.cleaning_log.append(f"Coluna '{column}' normalizada (min-max)")

        elif method == "zscore":
            mean = self.df[column].mean()
            std = self.df[column].std()
            self.df[column] = (self.df[column] - mean) / std
            self.cleaning_log.append(f"Coluna '{column}' normalizada (z-score)")

        print(f"✓ Coluna '{column}' normalizada usando {method}")
        return self.df

    def validate_email(self, column: str) -> Tuple[pd.DataFrame, int]:
        """
        Valida e-mails em uma coluna

        Args:
            column: Nome da coluna com e-mails

        Returns:
            Tupla (DataFrame apenas com e-mails válidos, número de inválidos)
        """
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if column not in self.df.columns:
            print(f"✗ Coluna '{column}' não encontrada")
            return self.df, 0

        valid_mask = self.df[column].str.match(email_pattern, na=False)
        invalid_count = (~valid_mask).sum()

        self.df = self.df[valid_mask]
        self.cleaning_log.append(f"E-mails inválidos removidos: {invalid_count}")
        print(f"✓ {invalid_count} e-mail(s) inválido(s) removido(s)")

        return self.df, invalid_count

    def validate_phone(self, column: str, pattern: Optional[str] = None) -> Tuple[pd.DataFrame, int]:
        """
        Valida telefones em uma coluna

        Args:
            column: Nome da coluna com telefones
            pattern: Regex customizado (None = padrão brasileiro)

        Returns:
            Tupla (DataFrame apenas com telefones válidos, número de inválidos)
        """
        if pattern is None:
            # Padrão brasileiro: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
            pattern = r"^\(\d{2}\)\s?\d{4,5}-?\d{4}$"

        if column not in self.df.columns:
            print(f"✗ Coluna '{column}' não encontrada")
            return self.df, 0

        valid_mask = self.df[column].str.match(pattern, na=False)
        invalid_count = (~valid_mask).sum()

        self.df = self.df[valid_mask]
        self.cleaning_log.append(f"Telefones inválidos removidos: {invalid_count}")
        print(f"✓ {invalid_count} telefone(s) inválido(s) removido(s)")

        return self.df, invalid_count

    def get_data_quality_report(self) -> Dict[str, Any]:
        """
        Gera relatório de qualidade dos dados

        Returns:
            Dicionário com métricas de qualidade
        """
        report = {
            "total_linhas": len(self.df),
            "total_colunas": len(self.df.columns),
            "valores_nulos": self.df.isnull().sum().to_dict(),
            "percentual_nulos": (self.df.isnull().sum() / len(self.df) * 100).to_dict(),
            "duplicados": self.df.duplicated().sum(),
            "tipos_dados": self.df.dtypes.to_dict(),
            "memoria_uso": self.df.memory_usage(deep=True).sum() / 1024**2,  # MB
            "estatisticas_numericas": self.df.describe().to_dict(),
            "log_limpeza": self.cleaning_log,
        }

        return report

    def print_quality_report(self):
        """Imprime relatório de qualidade dos dados de forma formatada"""
        report = self.get_data_quality_report()

        print("\n" + "=" * 80)
        print("RELATÓRIO DE QUALIDADE DOS DADOS")
        print("=" * 80)
        print(f"\n📊 Dimensões:")
        print(f"   Linhas: {report['total_linhas']}")
        print(f"   Colunas: {report['total_colunas']}")
        print(f"   Uso de memória: {report['memoria_uso']:.2f} MB")

        print(f"\n🔍 Duplicados: {report['duplicados']}")

        print(f"\n❌ Valores Nulos:")
        for col, count in report["valores_nulos"].items():
            if count > 0:
                perc = report["percentual_nulos"][col]
                print(f"   {col}: {count} ({perc:.1f}%)")

        if self.cleaning_log:
            print(f"\n📝 Histórico de Limpeza:")
            for i, log in enumerate(self.cleaning_log, 1):
                print(f"   {i}. {log}")

        print("=" * 80 + "\n")

    def reset_to_original(self) -> pd.DataFrame:
        """
        Restaura DataFrame ao estado original

        Returns:
            DataFrame original
        """
        self.df = self.original_df.copy()
        self.cleaning_log.append("DataFrame restaurado ao original")
        print("✓ Dados restaurados ao estado original")
        return self.df

    def get_cleaned_dataframe(self) -> pd.DataFrame:
        """
        Retorna o DataFrame limpo

        Returns:
            DataFrame limpo
        """
        return self.df
