"""
Sistema de Manipulação de Dados Excel com Banco de Dados
Arquivo principal com interface de menu interativo
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import DATABASE_PATH, EXCEL_FILE_PATH
from src.database import Database
from src.excel_handler import ExcelHandler
from src.data_cleaner import DataCleaner
from src.report_generator import ReportGenerator


class EventDataSystem:
    """Sistema principal de gerenciamento de dados de eventos"""

    def __init__(self):
        """Inicializa o sistema"""
        self.db = None
        self.excel_handler = None
        self.current_table = None

    def start(self):
        """Inicia o sistema"""
        self.print_header()
        self.db = Database(DATABASE_PATH)
        self.main_menu()

    def print_header(self):
        """Imprime cabeçalho do sistema"""
        print("\n" + "=" * 80)
        print(" " * 20 + "SISTEMA DE MANIPULAÇÃO DE DADOS")
        print(" " * 20 + "Excel + Banco de Dados SQLite")
        print("=" * 80 + "\n")

    def main_menu(self):
        """Menu principal do sistema"""
        while True:
            print("\n" + "─" * 80)
            print("MENU PRINCIPAL")
            print("─" * 80)
            print("📥 IMPORTAÇÃO E VISUALIZAÇÃO")
            print("1.  Importar dados do Excel para o banco")
            print("2.  Visualizar tabelas do banco")
            print("3.  Consultar dados de uma tabela")
            print("10. Ver preview do arquivo Excel")
            print("\n🧹 TRATAMENTO DE DADOS")
            print("11. Limpar dados (remover duplicados, nulos, etc)")
            print("12. Validar e-mails/telefones")
            print("13. Remover outliers")
            print("14. Normalizar dados")
            print("15. Relatório de qualidade dos dados")
            print("\n📊 RELATÓRIOS E ESTATÍSTICAS")
            print("4.  Visualizar estatísticas básicas")
            print("16. Gerar relatório completo (Excel)")
            print("17. Gerar relatório resumido (TXT)")
            print("18. Gerar relatório CSV")
            print("19. Tabela dinâmica (Pivot)")
            print("20. Relatório de frequência")
            print("\n💾 MANIPULAÇÃO DE DADOS")
            print("5.  Exportar dados para Excel")
            print("6.  Limpar e processar dados do Excel")
            print("7.  Inserir registro manualmente")
            print("8.  Atualizar registro")
            print("9.  Deletar registro")
            print("\n0.  Sair")
            print("─" * 80)

            choice = input("\nEscolha uma opção: ").strip()

            if choice == "1":
                self.import_excel_to_db()
            elif choice == "2":
                self.list_tables()
            elif choice == "3":
                self.query_table()
            elif choice == "4":
                self.show_statistics()
            elif choice == "5":
                self.export_to_excel()
            elif choice == "6":
                self.clean_excel_data()
            elif choice == "7":
                self.insert_record()
            elif choice == "8":
                self.update_record()
            elif choice == "9":
                self.delete_record()
            elif choice == "10":
                self.preview_excel()
            elif choice == "11":
                self.advanced_data_cleaning()
            elif choice == "12":
                self.validate_data()
            elif choice == "13":
                self.remove_outliers_menu()
            elif choice == "14":
                self.normalize_data_menu()
            elif choice == "15":
                self.data_quality_report()
            elif choice == "16":
                self.generate_excel_report()
            elif choice == "17":
                self.generate_text_report()
            elif choice == "18":
                self.generate_csv_report()
            elif choice == "19":
                self.generate_pivot_report()
            elif choice == "20":
                self.generate_frequency_report()
            elif choice == "0":
                self.exit_system()
                break
            else:
                print("✗ Opção inválida! Tente novamente.")

    def import_excel_to_db(self):
        """Importa dados do Excel para o banco de dados"""
        print("\n" + "─" * 80)
        print("IMPORTAR DADOS DO EXCEL")
        print("─" * 80)

        # Inicializa o manipulador de Excel
        self.excel_handler = ExcelHandler(EXCEL_FILE_PATH)

        if not self.excel_handler.load_excel():
            return

        # Mostra preview
        self.excel_handler.show_preview(5)

        # Pergunta o nome da tabela
        table_name = input("\nNome da tabela no banco (padrão: 'eventos'): ").strip()
        if not table_name:
            table_name = "eventos"

        # Pergunta se deve substituir ou adicionar
        print("\nO que fazer se a tabela já existir?")
        print("1. Substituir (replace)")
        print("2. Adicionar (append)")
        print("3. Falhar se existir (fail)")

        option = input("Escolha (padrão: 1): ").strip()
        if_exists = "replace"
        if option == "2":
            if_exists = "append"
        elif option == "3":
            if_exists = "fail"

        # Importa para o banco
        df = self.excel_handler.get_dataframe()
        if self.db.create_table_from_dataframe(df, table_name, if_exists):
            self.current_table = table_name
            print(f"\n✓ Importação concluída com sucesso!")

    def list_tables(self):
        """Lista todas as tabelas do banco"""
        print("\n" + "─" * 80)
        print("TABELAS DO BANCO DE DADOS")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada no banco")
            return

        for i, table in enumerate(tables, 1):
            stats = self.db.get_table_statistics(table)
            print(f"{i}. {table}")
            print(f"   Registros: {stats.get('total_registros', 0)}")
            print(f"   Colunas: {stats.get('total_colunas', 0)}")

    def query_table(self):
        """Consulta dados de uma tabela"""
        print("\n" + "─" * 80)
        print("CONSULTAR DADOS")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        # Mostra informações da tabela
        info = self.db.get_table_info(table_name)
        print(f"\nColunas da tabela '{table_name}':")
        for col in info:
            print(f"  - {col['name']} ({col['type']})")

        # Pergunta se quer filtrar
        use_filter = input("\nDeseja aplicar filtro WHERE? (s/n): ").strip().lower()
        where_clause = ""
        if use_filter == "s":
            where_clause = input("Digite a cláusula WHERE (ex: WHERE nome='João'): ").strip()

        # Busca os dados
        df = self.db.get_table_as_dataframe(table_name, where_clause)
        if df is not None:
            print(f"\n{len(df)} registro(s) encontrado(s):")
            print("\n" + "=" * 80)
            print(df.to_string())
            print("=" * 80)

    def show_statistics(self):
        """Mostra estatísticas de uma tabela"""
        print("\n" + "─" * 80)
        print("ESTATÍSTICAS")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        stats = self.db.get_table_statistics(table_name)
        print(f"\nEstatísticas da tabela '{table_name}':")
        print(f"Total de registros: {stats['total_registros']}")
        print(f"Total de colunas: {stats['total_colunas']}")
        print(f"\nColunas: {', '.join(stats['colunas'])}")

        # Estatísticas detalhadas usando pandas
        df = self.db.get_table_as_dataframe(table_name)
        if df is not None and not df.empty:
            print("\nEstatísticas numéricas:")
            print(df.describe())

    def export_to_excel(self):
        """Exporta dados do banco para Excel"""
        print("\n" + "─" * 80)
        print("EXPORTAR PARA EXCEL")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        output_name = input("Nome do arquivo de saída (sem extensão): ").strip()
        if not output_name:
            output_name = f"{table_name}_export"

        output_path = Path(__file__).parent.parent / f"{output_name}.xlsx"

        # Busca os dados e exporta
        df = self.db.get_table_as_dataframe(table_name)
        if df is not None:
            excel = ExcelHandler(output_path)
            if excel.export_to_excel(output_path, df, table_name):
                print(f"✓ Arquivo salvo em: {output_path}")

    def clean_excel_data(self):
        """Limpa e processa dados do Excel"""
        print("\n" + "─" * 80)
        print("LIMPAR DADOS DO EXCEL")
        print("─" * 80)

        self.excel_handler = ExcelHandler(EXCEL_FILE_PATH)
        if not self.excel_handler.load_excel():
            return

        print("\nDados antes da limpeza:")
        info = self.excel_handler.get_info()
        print(f"Linhas: {info['total_linhas']}")
        print(f"Colunas: {info['total_colunas']}")

        if self.excel_handler.clean_data():
            print("\nDados após a limpeza:")
            info = self.excel_handler.get_info()
            print(f"Linhas: {info['total_linhas']}")
            print(f"Colunas: {info['total_colunas']}")

            save = input("\nDeseja salvar os dados limpos no banco? (s/n): ").strip().lower()
            if save == "s":
                table_name = input("Nome da tabela: ").strip() or "eventos_limpos"
                df = self.excel_handler.get_dataframe()
                self.db.create_table_from_dataframe(df, table_name, "replace")

    def insert_record(self):
        """Insere um registro manualmente"""
        print("\n" + "─" * 80)
        print("INSERIR REGISTRO")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        # Mostra as colunas
        info = self.db.get_table_info(table_name)
        print(f"\nColunas da tabela '{table_name}':")
        for col in info:
            print(f"  - {col['name']}")

        # Coleta os dados
        data = {}
        print("\nDigite os valores (deixe vazio para pular):")
        for col in info:
            value = input(f"{col['name']}: ").strip()
            if value:
                data[col["name"]] = value

        if data:
            self.db.insert_record(table_name, data)

    def update_record(self):
        """Atualiza um registro"""
        print("\n" + "─" * 80)
        print("ATUALIZAR REGISTRO")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        where = input("Condição WHERE (ex: id = 1): ").strip()
        if not where:
            print("✗ Condição WHERE é obrigatória")
            return

        # Mostra as colunas
        info = self.db.get_table_info(table_name)
        print(f"\nColunas disponíveis:")
        for col in info:
            print(f"  - {col['name']}")

        # Coleta os novos valores
        data = {}
        print("\nDigite os novos valores:")
        while True:
            col = input("Nome da coluna (vazio para terminar): ").strip()
            if not col:
                break
            value = input(f"Novo valor para {col}: ").strip()
            if value:
                data[col] = value

        if data:
            self.db.update_record(table_name, data, where)

    def delete_record(self):
        """Deleta um registro"""
        print("\n" + "─" * 80)
        print("DELETAR REGISTRO")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        where = input("Condição WHERE (ex: id = 1): ").strip()
        if not where:
            print("✗ Condição WHERE é obrigatória")
            return

        confirm = input(f"⚠ Confirma a exclusão? (s/n): ").strip().lower()
        if confirm == "s":
            self.db.delete_record(table_name, where)

    def preview_excel(self):
        """Mostra preview do arquivo Excel"""
        print("\n" + "─" * 80)
        print("PREVIEW DO EXCEL")
        print("─" * 80)

        excel = ExcelHandler(EXCEL_FILE_PATH)
        if excel.load_excel():
            excel.show_preview(10)
            info = excel.get_info()
            print(f"\nInformações do arquivo:")
            print(f"Total de linhas: {info['total_linhas']}")
            print(f"Total de colunas: {info['total_colunas']}")
            print(f"Colunas: {', '.join(info['colunas'])}")
            print(f"Valores nulos por coluna:")
            for col, nulls in info["valores_nulos"].items():
                if nulls > 0:
                    print(f"  - {col}: {nulls}")

    def exit_system(self):
        """Encerra o sistema"""
        print("\n" + "=" * 80)
        print("Encerrando sistema...")
        if self.db:
            self.db.close()
        print("✓ Sistema encerrado com sucesso!")
        print("=" * 80 + "\n")

    # ============================================================================
    # NOVOS MÉTODOS - TRATAMENTO AVANÇADO DE DADOS
    # ============================================================================

    def advanced_data_cleaning(self):
        """Menu de limpeza avançada de dados"""
        print("\n" + "─" * 80)
        print("LIMPEZA AVANÇADA DE DADOS")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        df = self.db.get_table_as_dataframe(table_name)
        if df is None:
            return

        cleaner = DataCleaner(df)

        print("\nOpções de limpeza:")
        print("1. Remover duplicados")
        print("2. Tratar valores nulos (remover)")
        print("3. Tratar valores nulos (preencher)")
        print("4. Padronizar texto (minúsculas)")
        print("5. Padronizar texto (maiúsculas)")
        print("6. Remover caracteres especiais")
        print("7. Aplicar todas as limpezas básicas")

        option = input("\nEscolha uma opção: ").strip()

        if option == "1":
            cleaner.remove_duplicates()
        elif option == "2":
            cleaner.handle_missing_values(strategy="drop")
        elif option == "3":
            value = input("Valor para preencher: ").strip()
            cleaner.handle_missing_values(strategy="fill", fill_value=value)
        elif option == "4":
            cleaner.standardize_text(operation="lower")
        elif option == "5":
            cleaner.standardize_text(operation="upper")
        elif option == "6":
            cols = input("Colunas (separadas por vírgula): ").strip().split(",")
            cols = [c.strip() for c in cols]
            cleaner.remove_special_characters(cols)
        elif option == "7":
            cleaner.remove_duplicates()
            cleaner.handle_missing_values(strategy="drop")
            cleaner.standardize_text(operation="lower")

        cleaner.print_quality_report()

        save = input("\nSalvar dados limpos no banco? (s/n): ").strip().lower()
        if save == "s":
            new_table = input(f"Nome da nova tabela (Enter = substituir '{table_name}'): ").strip()
            if not new_table:
                new_table = table_name

            cleaned_df = cleaner.get_cleaned_dataframe()
            self.db.create_table_from_dataframe(cleaned_df, new_table, "replace")

    def validate_data(self):
        """Valida e-mails e telefones"""
        print("\n" + "─" * 80)
        print("VALIDAÇÃO DE DADOS")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        df = self.db.get_table_as_dataframe(table_name)
        if df is None:
            return

        cleaner = DataCleaner(df)

        print("\nColunas disponíveis:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i}. {col}")

        print("\nTipo de validação:")
        print("1. E-mail")
        print("2. Telefone")

        val_type = input("Escolha: ").strip()
        col_name = input("Nome da coluna: ").strip()

        if col_name not in df.columns:
            print("✗ Coluna não encontrada")
            return

        if val_type == "1":
            cleaner.validate_email(col_name)
        elif val_type == "2":
            cleaner.validate_phone(col_name)

        save = input("\nSalvar dados validados? (s/n): ").strip().lower()
        if save == "s":
            new_table = input("Nome da tabela: ").strip() or f"{table_name}_validado"
            validated_df = cleaner.get_cleaned_dataframe()
            self.db.create_table_from_dataframe(validated_df, new_table, "replace")

    def remove_outliers_menu(self):
        """Remove outliers de dados numéricos"""
        print("\n" + "─" * 80)
        print("REMOVER OUTLIERS")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        df = self.db.get_table_as_dataframe(table_name)
        if df is None:
            return

        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        if not numeric_cols:
            print("✗ Nenhuma coluna numérica encontrada")
            return

        print("\nColunas numéricas:")
        for i, col in enumerate(numeric_cols, 1):
            print(f"{i}. {col}")

        cols = input("\nColunas para remover outliers (separadas por vírgula): ").strip().split(",")
        cols = [c.strip() for c in cols if c.strip() in numeric_cols]

        if not cols:
            print("✗ Nenhuma coluna válida selecionada")
            return

        print("\nMétodo:")
        print("1. IQR (Interquartile Range)")
        print("2. Z-Score")

        method = "iqr" if input("Escolha (1/2): ").strip() == "1" else "zscore"

        cleaner = DataCleaner(df)
        cleaner.remove_outliers(cols, method=method)

        save = input("\nSalvar dados sem outliers? (s/n): ").strip().lower()
        if save == "s":
            new_table = input("Nome da tabela: ").strip() or f"{table_name}_sem_outliers"
            cleaned_df = cleaner.get_cleaned_dataframe()
            self.db.create_table_from_dataframe(cleaned_df, new_table, "replace")

    def normalize_data_menu(self):
        """Normaliza dados numéricos"""
        print("\n" + "─" * 80)
        print("NORMALIZAR DADOS")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        df = self.db.get_table_as_dataframe(table_name)
        if df is None:
            return

        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        if not numeric_cols:
            print("✗ Nenhuma coluna numérica encontrada")
            return

        print("\nColunas numéricas:")
        for i, col in enumerate(numeric_cols, 1):
            print(f"{i}. {col}")

        col = input("\nColuna para normalizar: ").strip()
        if col not in numeric_cols:
            print("✗ Coluna inválida")
            return

        print("\nMétodo:")
        print("1. Min-Max (0-1)")
        print("2. Z-Score")

        method = "minmax" if input("Escolha (1/2): ").strip() == "1" else "zscore"

        cleaner = DataCleaner(df)
        cleaner.normalize_column(col, method=method)

        save = input("\nSalvar dados normalizados? (s/n): ").strip().lower()
        if save == "s":
            new_table = input("Nome da tabela: ").strip() or f"{table_name}_normalizado"
            normalized_df = cleaner.get_cleaned_dataframe()
            self.db.create_table_from_dataframe(normalized_df, new_table, "replace")

    def data_quality_report(self):
        """Gera relatório de qualidade dos dados"""
        print("\n" + "─" * 80)
        print("RELATÓRIO DE QUALIDADE")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        df = self.db.get_table_as_dataframe(table_name)
        if df is None:
            return

        cleaner = DataCleaner(df)
        cleaner.print_quality_report()

    # ============================================================================
    # NOVOS MÉTODOS - GERAÇÃO DE RELATÓRIOS
    # ============================================================================

    def generate_excel_report(self):
        """Gera relatório completo em Excel"""
        print("\n" + "─" * 80)
        print("GERAR RELATÓRIO EXCEL")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        df = self.db.get_table_as_dataframe(table_name)
        if df is None:
            return

        report_name = input("Nome do relatório (sem extensão): ").strip() or table_name
        output_path = Path(__file__).parent.parent / f"relatorios/{report_name}_completo.xlsx"

        report_gen = ReportGenerator(df, report_name)
        report_gen.generate_excel_report(output_path, include_stats=True)

    def generate_text_report(self):
        """Gera relatório resumido em texto"""
        print("\n" + "─" * 80)
        print("GERAR RELATÓRIO TEXTO")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        df = self.db.get_table_as_dataframe(table_name)
        if df is None:
            return

        report_name = input("Nome do relatório (sem extensão): ").strip() or table_name
        output_path = Path(__file__).parent.parent / f"relatorios/{report_name}_resumido.txt"

        report_gen = ReportGenerator(df, report_name)
        report_gen.generate_summary_report(output_path)

        print("\n" + "=" * 80)
        report_gen.print_summary()

    def generate_csv_report(self):
        """Gera relatório em CSV"""
        print("\n" + "─" * 80)
        print("GERAR RELATÓRIO CSV")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        df = self.db.get_table_as_dataframe(table_name)
        if df is None:
            return

        report_name = input("Nome do relatório (sem extensão): ").strip() or table_name

        print("\nSeparador:")
        print("1. Vírgula (,)")
        print("2. Ponto e vírgula (;)")
        print("3. Tab (\\t)")

        sep_choice = input("Escolha (padrão: 1): ").strip()
        separator = "," if sep_choice != "2" and sep_choice != "3" else (";" if sep_choice == "2" else "\t")

        output_path = Path(__file__).parent.parent / f"relatorios/{report_name}.csv"

        report_gen = ReportGenerator(df, report_name)
        report_gen.generate_csv_report(output_path, separator)

    def generate_pivot_report(self):
        """Gera tabela dinâmica (pivot)"""
        print("\n" + "─" * 80)
        print("GERAR TABELA DINÂMICA")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        df = self.db.get_table_as_dataframe(table_name)
        if df is None:
            return

        print("\nColunas disponíveis:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i}. {col}")

        index_col = input("\nColuna para LINHAS (índice): ").strip()
        columns_col = input("Coluna para COLUNAS: ").strip()
        values_col = input("Coluna para VALORES: ").strip()

        if index_col not in df.columns or columns_col not in df.columns or values_col not in df.columns:
            print("✗ Uma ou mais colunas inválidas")
            return

        print("\nFunção de agregação:")
        print("1. Soma (sum)")
        print("2. Média (mean)")
        print("3. Contagem (count)")
        print("4. Mínimo (min)")
        print("5. Máximo (max)")

        agg_choice = input("Escolha (padrão: 1): ").strip()
        agg_func = {"1": "sum", "2": "mean", "3": "count", "4": "min", "5": "max"}.get(agg_choice, "sum")

        report_gen = ReportGenerator(df, table_name)

        save = input("\nSalvar em arquivo? (s/n): ").strip().lower()
        output_path = None
        if save == "s":
            report_name = input("Nome do arquivo (sem extensão): ").strip() or f"{table_name}_pivot"
            output_path = Path(__file__).parent.parent / f"relatorios/{report_name}.xlsx"

        report_gen.generate_pivot_report(index_col, columns_col, values_col, agg_func, output_path)

    def generate_frequency_report(self):
        """Gera relatório de frequência"""
        print("\n" + "─" * 80)
        print("GERAR RELATÓRIO DE FREQUÊNCIA")
        print("─" * 80)

        tables = self.db.get_table_names()
        if not tables:
            print("✗ Nenhuma tabela encontrada")
            return

        print("Tabelas disponíveis:")
        for i, table in enumerate(tables, 1):
            print(f"{i}. {table}")

        table_name = input("\nNome da tabela: ").strip()
        if table_name not in tables:
            print("✗ Tabela não encontrada")
            return

        df = self.db.get_table_as_dataframe(table_name)
        if df is None:
            return

        cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
        if not cat_cols:
            print("✗ Nenhuma coluna categórica encontrada")
            return

        print("\nColunas categóricas disponíveis:")
        for i, col in enumerate(cat_cols, 1):
            print(f"{i}. {col}")

        cols_input = input("\nColunas para análise (separadas por vírgula, ou 'todas'): ").strip()

        if cols_input.lower() == "todas":
            selected_cols = cat_cols
        else:
            selected_cols = [c.strip() for c in cols_input.split(",") if c.strip() in cat_cols]

        if not selected_cols:
            print("✗ Nenhuma coluna válida selecionada")
            return

        report_gen = ReportGenerator(df, table_name)

        save = input("\nSalvar em arquivo? (s/n): ").strip().lower()
        output_path = None
        if save == "s":
            report_name = input("Nome do arquivo (sem extensão): ").strip() or f"{table_name}_frequencia"
            output_path = Path(__file__).parent.parent / f"relatorios/{report_name}.xlsx"

        report_gen.generate_frequency_report(selected_cols, output_path)
        if self.db:
            self.db.close()
        print("✓ Sistema encerrado com sucesso!")
        print("=" * 80 + "\n")


def main():
    """Função principal"""
    try:
        system = EventDataSystem()
        system.start()
    except KeyboardInterrupt:
        print("\n\n✗ Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"\n✗ Erro inesperado: {e}")


if __name__ == "__main__":
    main()
