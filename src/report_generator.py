"""
Módulo para geração de relatórios em diversos formatos
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Any
from datetime import datetime
import csv


class ReportGenerator:
    """Classe para gerar relatórios em diversos formatos"""

    def __init__(self, df: pd.DataFrame, report_name: str = "relatorio"):
        """
        Inicializa o gerador de relatórios

        Args:
            df: DataFrame com os dados
            report_name: Nome base para os relatórios
        """
        self.df = df
        self.report_name = report_name
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate_summary_report(self, output_path: Optional[Path] = None) -> str:
        """
        Gera relatório resumido em texto

        Args:
            output_path: Caminho para salvar (None = retorna string)

        Returns:
            Texto do relatório
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append(f"RELATÓRIO RESUMIDO - {self.report_name.upper()}")
        report_lines.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        report_lines.append("=" * 80)

        # Informações gerais
        report_lines.append(f"\n📊 INFORMAÇÕES GERAIS")
        report_lines.append(f"   Total de Registros: {len(self.df)}")
        report_lines.append(f"   Total de Colunas: {len(self.df.columns)}")
        report_lines.append(f"   Colunas: {', '.join(self.df.columns)}")

        # Valores nulos
        null_counts = self.df.isnull().sum()
        if null_counts.sum() > 0:
            report_lines.append(f"\n❌ VALORES AUSENTES")
            for col, count in null_counts.items():
                if count > 0:
                    perc = (count / len(self.df)) * 100
                    report_lines.append(f"   {col}: {count} ({perc:.1f}%)")

        # Duplicados
        duplicates = self.df.duplicated().sum()
        report_lines.append(f"\n🔄 DUPLICADOS: {duplicates}")

        # Estatísticas numéricas
        numeric_cols = self.df.select_dtypes(include=["int64", "float64"]).columns
        if len(numeric_cols) > 0:
            report_lines.append(f"\n📈 ESTATÍSTICAS NUMÉRICAS")
            stats = self.df[numeric_cols].describe()
            report_lines.append(stats.to_string())

        # Estatísticas categóricas
        cat_cols = self.df.select_dtypes(include=["object"]).columns
        if len(cat_cols) > 0:
            report_lines.append(f"\n📝 ESTATÍSTICAS CATEGÓRICAS")
            for col in cat_cols[:5]:  # Limita a 5 colunas
                unique_count = self.df[col].nunique()
                most_common = self.df[col].mode()[0] if not self.df[col].mode().empty else "N/A"
                report_lines.append(f"   {col}:")
                report_lines.append(f"      Valores únicos: {unique_count}")
                report_lines.append(f"      Mais comum: {most_common}")

        report_lines.append("\n" + "=" * 80)

        report_text = "\n".join(report_lines)

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report_text)
            print(f"✓ Relatório texto salvo em: {output_path}")

        return report_text

    def generate_excel_report(self, output_path: Path, include_stats: bool = True) -> bool:
        """
        Gera relatório completo em Excel com múltiplas abas

        Args:
            output_path: Caminho do arquivo Excel
            include_stats: Se True, inclui aba com estatísticas

        Returns:
            True se sucesso
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                # Aba 1: Dados completos
                self.df.to_excel(writer, sheet_name="Dados", index=False)

                # Aba 2: Estatísticas
                if include_stats:
                    stats_df = self.df.describe(include="all").T
                    stats_df.to_excel(writer, sheet_name="Estatísticas")

                # Aba 3: Valores nulos
                null_df = pd.DataFrame(
                    {
                        "Coluna": self.df.columns,
                        "Valores Nulos": self.df.isnull().sum().values,
                        "Percentual": (self.df.isnull().sum() / len(self.df) * 100).values,
                    }
                )
                null_df.to_excel(writer, sheet_name="Valores Nulos", index=False)

                # Aba 4: Tipos de dados
                types_df = pd.DataFrame({"Coluna": self.df.columns, "Tipo": self.df.dtypes.values})
                types_df.to_excel(writer, sheet_name="Tipos de Dados", index=False)

            print(f"✓ Relatório Excel salvo em: {output_path}")
            return True

        except Exception as e:
            print(f"✗ Erro ao gerar relatório Excel: {e}")
            return False

    def generate_csv_report(self, output_path: Path, separator: str = ",") -> bool:
        """
        Gera relatório em formato CSV

        Args:
            output_path: Caminho do arquivo CSV
            separator: Separador (padrão: vírgula)

        Returns:
            True se sucesso
        """
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            self.df.to_csv(output_path, sep=separator, index=False, encoding="utf-8-sig")
            print(f"✓ Relatório CSV salvo em: {output_path}")
            return True

        except Exception as e:
            print(f"✗ Erro ao gerar relatório CSV: {e}")
            return False

    def generate_pivot_report(
        self, index: str, columns: str, values: str, aggfunc: str = "sum", output_path: Optional[Path] = None
    ) -> pd.DataFrame:
        """
        Gera relatório de tabela dinâmica (pivot)

        Args:
            index: Coluna para índice
            columns: Coluna para colunas
            values: Coluna para valores
            aggfunc: Função de agregação ('sum', 'mean', 'count', etc)
            output_path: Caminho para salvar (opcional)

        Returns:
            DataFrame com tabela dinâmica
        """
        try:
            pivot = pd.pivot_table(self.df, index=index, columns=columns, values=values, aggfunc=aggfunc, fill_value=0)

            print(f"✓ Tabela dinâmica gerada")
            print(pivot)

            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                pivot.to_excel(output_path)
                print(f"✓ Tabela dinâmica salva em: {output_path}")

            return pivot

        except Exception as e:
            print(f"✗ Erro ao gerar tabela dinâmica: {e}")
            return pd.DataFrame()

    def generate_comparison_report(
        self, group_column: str, compare_columns: List[str], output_path: Optional[Path] = None
    ) -> pd.DataFrame:
        """
        Gera relatório de comparação entre grupos

        Args:
            group_column: Coluna para agrupar
            compare_columns: Colunas numéricas para comparar
            output_path: Caminho para salvar (opcional)

        Returns:
            DataFrame com comparações
        """
        try:
            comparison = self.df.groupby(group_column)[compare_columns].agg(["mean", "sum", "count"])

            print(f"✓ Relatório de comparação gerado")
            print(comparison)

            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                comparison.to_excel(output_path)
                print(f"✓ Relatório salvo em: {output_path}")

            return comparison

        except Exception as e:
            print(f"✗ Erro ao gerar relatório de comparação: {e}")
            return pd.DataFrame()

    def generate_frequency_report(
        self, columns: List[str], output_path: Optional[Path] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Gera relatório de frequência para colunas categóricas

        Args:
            columns: Lista de colunas categóricas
            output_path: Caminho para salvar (opcional)

        Returns:
            Dicionário com DataFrames de frequência por coluna
        """
        frequency_reports = {}

        for col in columns:
            if col in self.df.columns:
                freq = self.df[col].value_counts().reset_index()
                freq.columns = [col, "Frequência"]
                freq["Percentual"] = (freq["Frequência"] / len(self.df) * 100).round(2)
                frequency_reports[col] = freq

                print(f"\n📊 Frequência - {col}:")
                print(freq.head(10))

        if output_path and frequency_reports:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                for col, freq_df in frequency_reports.items():
                    sheet_name = col[:31]  # Excel limita a 31 caracteres
                    freq_df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"\n✓ Relatório de frequência salvo em: {output_path}")

        return frequency_reports

    def generate_missing_data_report(self, output_path: Optional[Path] = None) -> pd.DataFrame:
        """
        Gera relatório detalhado sobre dados ausentes

        Args:
            output_path: Caminho para salvar (opcional)

        Returns:
            DataFrame com análise de dados ausentes
        """
        missing_data = pd.DataFrame(
            {
                "Coluna": self.df.columns,
                "Total_Nulos": self.df.isnull().sum().values,
                "Percentual": (self.df.isnull().sum() / len(self.df) * 100).round(2).values,
                "Tipo_Dados": self.df.dtypes.values,
            }
        )

        missing_data = missing_data[missing_data["Total_Nulos"] > 0].sort_values("Percentual", ascending=False)

        print("\n📋 RELATÓRIO DE DADOS AUSENTES")
        print(missing_data.to_string(index=False))

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            missing_data.to_excel(output_path, index=False)
            print(f"\n✓ Relatório salvo em: {output_path}")

        return missing_data

    def generate_custom_filter_report(
        self, filters: Dict[str, Any], output_path: Optional[Path] = None
    ) -> pd.DataFrame:
        """
        Gera relatório com filtros customizados

        Args:
            filters: Dicionário com filtros {coluna: valor}
            output_path: Caminho para salvar (opcional)

        Returns:
            DataFrame filtrado
        """
        filtered_df = self.df.copy()

        for col, value in filters.items():
            if col in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[col] == value]

        print(f"✓ Filtros aplicados: {len(filtered_df)} registros encontrados")

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            filtered_df.to_excel(output_path, index=False)
            print(f"✓ Relatório filtrado salvo em: {output_path}")

        return filtered_df

    def print_summary(self):
        """Imprime resumo simples na tela"""
        print(self.generate_summary_report())
