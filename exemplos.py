"""
Exemplos de uso das funcionalidades de tratamento de dados e relatórios
"""

from pathlib import Path
import sys
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

from src.data_cleaner import DataCleaner
from src.report_generator import ReportGenerator


def exemplo_limpeza_basica():
    """Demonstra limpeza básica de dados"""
    print("\n" + "=" * 80)
    print("EXEMPLO 1: LIMPEZA BÁSICA DE DADOS")
    print("=" * 80)

    # Criar dados de exemplo com problemas
    data = {
        "nome": ["João Silva", "MARIA SANTOS", "  Pedro Lima  ", "João Silva", "Ana Costa", None],
        "email": ["joao@email.com", "maria@email", "pedro@email.com", "joao@email.com", "ana@email.com", "invalido"],
        "idade": [25, 30, None, 25, 28, 150],  # 150 é outlier
        "telefone": ["(11) 99999-9999", "11999999999", "(21) 88888-8888", "(11) 99999-9999", "(31) 77777-7777", None],
    }

    df = pd.DataFrame(data)
    print("\n📊 Dados Originais:")
    print(df)

    # Criar objeto de limpeza
    cleaner = DataCleaner(df)

    # 1. Remover duplicados
    cleaner.remove_duplicates()

    # 2. Tratar valores nulos
    cleaner.handle_missing_values(strategy="drop")

    # 3. Padronizar texto
    cleaner.standardize_text(operation="title")

    # 4. Relatório de qualidade
    cleaner.print_quality_report()

    # Obter dados limpos
    df_limpo = cleaner.get_cleaned_dataframe()
    print("\n✨ Dados Limpos:")
    print(df_limpo)


def exemplo_validacao():
    """Demonstra validação de dados"""
    print("\n" + "=" * 80)
    print("EXEMPLO 2: VALIDAÇÃO DE E-MAILS")
    print("=" * 80)

    data = {
        "cliente": ["João", "Maria", "Pedro", "Ana"],
        "email": ["joao@email.com", "maria@email", "pedro@empresa.com.br", "ana@teste.co"],
    }

    df = pd.DataFrame(data)
    print("\n📧 E-mails Originais:")
    print(df)

    cleaner = DataCleaner(df)
    cleaner.validate_email("email")

    df_validado = cleaner.get_cleaned_dataframe()
    print("\n✅ E-mails Válidos:")
    print(df_validado)


def exemplo_outliers():
    """Demonstra remoção de outliers"""
    print("\n" + "=" * 80)
    print("EXEMPLO 3: REMOÇÃO DE OUTLIERS")
    print("=" * 80)

    data = {
        "produto": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
        "preco": [100, 105, 98, 102, 101, 99, 103, 104, 1000, 97],  # 1000 é outlier
    }

    df = pd.DataFrame(data)
    print("\n💰 Preços com Outlier:")
    print(df)
    print(f"Média: {df['preco'].mean():.2f}")

    cleaner = DataCleaner(df)
    cleaner.remove_outliers(["preco"], method="iqr", threshold=1.5)

    df_sem_outliers = cleaner.get_cleaned_dataframe()
    print("\n✨ Preços Sem Outliers:")
    print(df_sem_outliers)
    print(f"Nova Média: {df_sem_outliers['preco'].mean():.2f}")


def exemplo_normalizacao():
    """Demonstra normalização de dados"""
    print("\n" + "=" * 80)
    print("EXEMPLO 4: NORMALIZAÇÃO DE DADOS")
    print("=" * 80)

    data = {"aluno": ["João", "Maria", "Pedro", "Ana"], "nota": [85, 95, 70, 90]}

    df = pd.DataFrame(data)
    print("\n📚 Notas Originais:")
    print(df)

    cleaner = DataCleaner(df)
    cleaner.normalize_column("nota", method="minmax")

    df_normalizado = cleaner.get_cleaned_dataframe()
    print("\n📊 Notas Normalizadas (0-1):")
    print(df_normalizado)


def exemplo_relatorio_excel():
    """Demonstra geração de relatório Excel"""
    print("\n" + "=" * 80)
    print("EXEMPLO 5: GERAR RELATÓRIO EXCEL")
    print("=" * 80)

    data = {
        "produto": ["Mouse", "Teclado", "Monitor", "Mouse", "Teclado", "Monitor"],
        "categoria": ["Hardware", "Hardware", "Hardware", "Hardware", "Hardware", "Hardware"],
        "vendas": [150, 200, 80, 160, 210, 85],
        "preco": [45.90, 89.90, 599.90, 49.90, 95.90, 649.90],
    }

    df = pd.DataFrame(data)
    print("\n📊 Dados de Vendas:")
    print(df)

    report_gen = ReportGenerator(df, "vendas_exemplo")

    output_path = Path(__file__).parent / "relatorios" / "exemplo_vendas.xlsx"
    report_gen.generate_excel_report(output_path, include_stats=True)

    print(f"\n✅ Relatório salvo em: {output_path}")


def exemplo_tabela_dinamica():
    """Demonstra criação de tabela dinâmica"""
    print("\n" + "=" * 80)
    print("EXEMPLO 6: TABELA DINÂMICA (PIVOT)")
    print("=" * 80)

    data = {
        "vendedor": ["João", "Maria", "João", "Maria", "João", "Maria"],
        "produto": ["Mouse", "Mouse", "Teclado", "Teclado", "Monitor", "Monitor"],
        "vendas": [10, 15, 8, 12, 3, 5],
    }

    df = pd.DataFrame(data)
    print("\n💼 Dados de Vendas por Vendedor:")
    print(df)

    report_gen = ReportGenerator(df, "vendas_por_vendedor")
    pivot = report_gen.generate_pivot_report(index="vendedor", columns="produto", values="vendas", aggfunc="sum")


def exemplo_frequencia():
    """Demonstra relatório de frequência"""
    print("\n" + "=" * 80)
    print("EXEMPLO 7: RELATÓRIO DE FREQUÊNCIA")
    print("=" * 80)

    data = {
        "cidade": [
            "São Paulo",
            "Rio de Janeiro",
            "São Paulo",
            "Belo Horizonte",
            "São Paulo",
            "Rio de Janeiro",
            "Curitiba",
            "São Paulo",
        ],
        "estado": ["SP", "RJ", "SP", "MG", "SP", "RJ", "PR", "SP"],
    }

    df = pd.DataFrame(data)
    print("\n🌎 Dados de Localização:")
    print(df)

    report_gen = ReportGenerator(df, "localizacoes")
    freq_reports = report_gen.generate_frequency_report(["cidade", "estado"])


def exemplo_completo():
    """Workflow completo de análise de dados"""
    print("\n" + "=" * 80)
    print("EXEMPLO 8: WORKFLOW COMPLETO")
    print("=" * 80)

    # Dados simulados de eventos
    data = {
        "participante": ["João Silva", "MARIA SANTOS", "João Silva", "  Pedro Lima  ", "Ana Costa"],
        "email": ["joao@email.com", "maria@email.com", "joao@email.com", "pedro@email.com", "ana@email"],
        "idade": [25, 30, 25, 28, 150],  # 150 é outlier
        "cidade": ["São Paulo", "Rio", "São Paulo", "Belo Horizonte", "São Paulo"],
        "presenca": ["Sim", "Sim", "Sim", "Não", "Sim"],
    }

    df = pd.DataFrame(data)
    print("\n📋 Dados Originais do Evento:")
    print(df)

    # Passo 1: Limpeza
    print("\n🧹 PASSO 1: Limpando dados...")
    cleaner = DataCleaner(df)
    cleaner.remove_duplicates()
    cleaner.handle_missing_values(strategy="drop")
    cleaner.standardize_text(operation="title")

    # Passo 2: Validação
    print("\n✅ PASSO 2: Validando dados...")
    cleaner.validate_email("email")

    # Passo 3: Remover outliers
    print("\n📊 PASSO 3: Removendo outliers...")
    cleaner.remove_outliers(["idade"], method="iqr")

    # Passo 4: Relatório de qualidade
    print("\n📈 PASSO 4: Relatório de qualidade...")
    cleaner.print_quality_report()

    # Passo 5: Obter dados limpos
    df_final = cleaner.get_cleaned_dataframe()
    print("\n✨ DADOS FINAIS:")
    print(df_final)

    # Passo 6: Gerar relatórios
    print("\n📄 PASSO 6: Gerando relatórios...")
    report_gen = ReportGenerator(df_final, "evento_final")

    # Relatório texto
    report_gen.print_summary()

    # Relatório de frequência
    report_gen.generate_frequency_report(["cidade", "presenca"])


if __name__ == "__main__":
    print("\n" + "🚀" * 40)
    print("EXEMPLOS DE USO - SISTEMA DE MANIPULAÇÃO DE DADOS")
    print("🚀" * 40)

    # Execute os exemplos desejados
    exemplo_limpeza_basica()
    exemplo_validacao()
    exemplo_outliers()
    exemplo_normalizacao()
    exemplo_relatorio_excel()
    exemplo_tabela_dinamica()
    exemplo_frequencia()
    exemplo_completo()

    print("\n" + "✅" * 40)
    print("TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO!")
    print("✅" * 40 + "\n")
