# Projeto de Manipulação de Dados Excel com Banco de Dados + Django

Sistema completo e profissional para tratamento, manipulação e análise de dados de arquivos Excel utilizando banco de dados SQLite, com interface web Django e painel administrativo.

## 🌟 Novidade: Interface Web com Django!

✨ **Agora com sistema web completo!**
- 🌐 Interface web moderna e responsiva
- 🔧 Painel administrativo Django
- 📤 Upload de arquivos Excel via web
- 📊 Dashboard com estatísticas
- 🎨 Interface visual profissional

## 🎯 Funcionalidades Principais

### 📥 Importação e Visualização
- ✅ Importar dados de arquivos Excel para banco de dados
- ✅ Visualizar estrutura e conteúdo das tabelas
- ✅ Preview de dados do Excel
- ✅ Consultas com filtros personalizados

### 🧹 Tratamento Avançado de Dados
- ✅ Remover duplicados automaticamente
- ✅ Tratar valores nulos (múltiplas estratégias)
- ✅ Padronizar texto (maiúsculas, minúsculas, capitalização)
- ✅ Validar e-mails e telefones
- ✅ Remover outliers (IQR e Z-Score)
- ✅ Normalizar dados numéricos
- ✅ Relatório de qualidade dos dados

### 📊 Geração de Relatórios
- ✅ Relatório Excel completo (múltiplas abas)
- ✅ Relatório resumido em texto
- ✅ Exportação para CSV
- ✅ Tabelas dinâmicas (Pivot)
- ✅ Relatório de frequência
- ✅ Análise de dados ausentes
- ✅ Estatísticas descritivas

### 💾 Manipulação de Dados
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Exportar dados para Excel
- ✅ Filtros e consultas SQL
- ✅ Backup de dados

## Estrutura do Projeto

```
projeto_evento/
├── src/                    # Módulos Python (CLI)
│   ├── database.py         # Gerenciamento do banco de dados SQLite
│   ├── excel_handler.py    # Manipulação de arquivos Excel
│   ├── data_cleaner.py     # Limpeza e tratamento avançado
│   ├── report_generator.py # Geração de relatórios
│   └── main.py            # Interface CLI com menu
├── webapp/                # 🆕 Aplicação Django (Web)
│   ├── manage.py          # Utilitário Django
│   ├── core/             # Configurações do projeto
│   │   ├── settings.py
│   │   └── urls.py
│   └── eventos/          # App de eventos
│       ├── models.py     # Modelos de dados
│       ├── admin.py      # Admin customizado
│       ├── views.py      # Controllers
│       ├── urls.py
│       └── templates/    # Templates HTML
├── data/                  # Bancos de dados
├── relatorios/           # Relatórios gerados
├── media/                # 🆕 Uploads web
├── config.py             # Configurações do projeto
├── requirements.txt      # Dependências Python
├── DJANGO_GUIDE.md       # 🆕 Documentação Django
├── INICIO_RAPIDO.md      # 🆕 Guia de inicialização
├── MELHORIAS.md         # Documentação detalhada das melhorias
└── README.md            # Este arquivo
```

## Instalação

1. As dependências já foram instaladas automaticamente no ambiente virtual

2. Ou instale manualmente:
```bash
pip install -r requirements.txt
```

## Como Usar

### 🌐 Opção 1: Interface Web Django (Recomendado)

```bash
# Inicialização automática
.\iniciar_django.ps1

# Ou manual:
cd webapp
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Acesse:**
- Dashboard: http://localhost:8000/
- Admin: http://localhost:8000/admin/

📖 **Guia completo**: [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

### 💻 Opção 2: Interface CLI (Terminal)

Execute o arquivo principal:
``**[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - 🆕 Guia rápido para iniciar o Django
- **[DJANGO_GUIDE.md](DJANGO_GUIDE.md)** - 🆕 Documentação completa do Django
- **[MELHORIAS.md](MELHORIAS.md)** - Documentação completa de todas as funcionalidades CLI
- **[GUIA_RAPIDO.txt](GUIA_RAPIDO.txt)** - Referência rápida de comando
python src/main.py
```

### Menu Organizado

O sistema apresenta um mene análise de dados
- **openpyxl**: Leitura/escrita de arquivos Excel (.xlsx)
- **sqlalchemy**: ORM para banco de dados SQLite
- **python-dotenv**: Gerenciamento de variáveis de ambiente
- **numpy**: Operações numéricas (instalado com pandas)

## 📚 Documentação Adicional

- [MELHORIAS.md](MELHORIAS.md) - Documentação completa de todas as funcionalidades
- Veja exemplos de workflows e casos de uso
- Dicas de uso e boas práticas

## 🎓 Recursos de Aprendizado

Este projeto implementa conceitos de:
- Manipulação de dados com Pandas
- Banco de dados relacional (SQLite)
- Limpeza e tratamento de dados
- Análise estatística
- **🆕 Framework Django (MVT)**
- **🆕 Django Admin customizado**
- **🆕 Templates e frontend web**
- **🆕 Upload e processamento de arquivos**
- **🆕 Autenticação e permissões**

## 🌟 Diferenciais do Sistema

✅ **Dual Interface**: CLI + Web Django  
✅ **Admin Profissional**: Interface visual completa  
✅ **Integração Total**: Módulos compartilhados entre CLI e Web  
✅ **Tratamento Avançado**: Limpeza, validação, outliers  
✅ **Múltiplos Formatos**: Excel, CSV, TXT, PDF  
✅ **Relatórios Ricos**: Estatísticas e análises detalhadas  
✅ **Import/Export**: Upload direto via web  
✅ **Responsivo**: Funciona em desktop e mobile
- Validação de dados
- Geração de relatórios
- Programação orientada a objetos

## 🤝 Contribuindo

Sugestões de melhorias futuras:
- Visualizações gráficas (matplotlib/plotly)
- Interface gráfica (GUI)
- Exportação para PDF
- Análises preditivas
- API REST
- Sistema de backup automático
- Visualizar tabelas existentes
- Consultar e filtrar dados
- Preview do arquivo Excel

#### 🧹 Tratamento de Dados
- Limpeza avançada (duplicados, nulos, formatação)
- Validação de e-mails e telefones
- Remoção de outliers estatísticos
- Normalização de dados numéricos
- Relatório de qualidade

#### 📊 Relatórios e Estatísticas
- Estatísticas básicas e avançadas
- Relatórios em Excel, TXT e CSV
- Tabelas dinâmicas (Pivot)
- Análise de frequência

#### 💾 Manipulação de Dados
- Inserir, atualizar e deletar registros
- Exportar para Excel
- Backup de tabelas

### Exemplos Práticos

**Exemplo 1: Limpar e Validar Dados**
```
Menu → 11 (Limpar dados avançados)
→ Escolher tabela
→ Opção 7 (Aplicar todas as limpezas)
→ Salvar em nova tabela

Menu → 12 (Validar e-mails/telefones)
→ Validar e-mails
→ Salvar dados validados
```

**Exemplo 2: Gerar Relatório Completo**
```
Menu → 16 (Gerar relatório Excel)
→ Escolher tabela
→ Relatório salvo em /relatorios/
```

**Exemplo 3: Criar Tabela Dinâmica**
```
Menu → 19 (Tabela dinâmica)
→ Definir linhas, colunas e valores
→ Escolher agregação (soma, média)
→ Visualizar ou salvar
```

## Dependências

- **pandas**: Manipulação de dados
- **openpyxl**: Leitura/escrita de arquivos Excel
- **sqlalchemy**: ORM para banco de dados
- **python-dotenv**: Gerenciamento de variáveis de ambiente
