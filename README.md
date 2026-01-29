# Sistema de Gerenciamento de Eventos e Participantes

## 📋 Descrição Profissional do Sistema

**Backend de Eventos** é uma plataforma enterprise completa para gerenciamento de eventos, participantes e dados, desenvolvida com foco em escalabilidade, qualidade de dados e experiência do usuário. O sistema combina processamento avançado de dados, interface web moderna e ferramentas CLI robustas para oferecer uma solução completa de gestão de eventos.

### 🎯 Propósito e Aplicações

O sistema foi projetado para organizações que necessitam:
- **Gestão Centralizada de Eventos**: Controle completo do ciclo de vida de eventos, desde planejamento até conclusão
- **Processamento de Grandes Volumes**: Importação e tratamento de milhares de registros de participantes via Excel
- **Qualidade de Dados**: Validação, limpeza e normalização automatizada de informações
- **Análise e Relatórios**: Geração de insights através de relatórios detalhados e dashboards interativos
- **Integração Multi-canal**: Suporte para operações via interface web e linha de comando

## 🏗️ Arquitetura e Tecnologias

### Stack Tecnológico
- **Backend Framework**: Django 5.0+ (Python)
- **ORM/Database**: SQLAlchemy + SQLite (produção-ready, pode migrar para PostgreSQL/MySQL)
- **Data Processing**: Pandas, NumPy para análise e manipulação de dados
- **File Handling**: OpenPyXL para processamento Excel
- **Frontend**: Templates Django com Bootstrap 5, interface responsiva
- **Autenticação**: Django Auth com controle de permissões

### Padrões Arquiteturais
- **MVT (Model-View-Template)**: Padrão Django para separação de responsabilidades
- **ORM Pattern**: Abstração de banco de dados com modelos Django
- **Repository Pattern**: Módulos isolados para operações de dados (src/)
- **Service Layer**: Lógica de negócio separada em serviços especializados
- **Dual Interface**: Web UI + CLI para máxima flexibilidade operacional

## 🎯 Funcionalidades Principais

### 🎪 Gestão de Eventos
- **CRUD Completo**: Criação, leitura, atualização e exclusão de eventos
- **Categorização**: Sistema flexível de categorias com códigos de cores
- **Ciclo de Vida**: Rastreamento de status (Planejamento → Confirmado → Em Andamento → Concluído)
- **Controle de Capacidade**: Gestão automática de vagas e taxa de ocupação
- **Multi-localização**: Suporte para eventos em diferentes cidades e estados
- **Precificação**: Gestão de valores de ingressos e receitas

### 👥 Gestão de Participantes/Clientes
- **Cadastro Único**: Sistema de clientes com informações centralizadas
- **Validação Avançada**: Verificação automática de e-mails, telefones e CPF
- **Deduplicação**: Identificação e remoção de registros duplicados
- **Histórico Completo**: Rastreamento de todas as participações por cliente
- **Tipos de Ingresso**: Suporte para VIP, Comum, Staff, Palestrante
- **Status Tracking**: Pendente, Confirmado, Presente, Ausente, Cancelado

### 📥 Importação e Integração de Dados
- ✅ **Upload em Massa**: Importação de milhares de registros via Excel (.xlsx)
- ✅ **Mapeamento Inteligente**: Reconhecimento automático de colunas e formatos
- ✅ **Validação em Tempo Real**: Verificação de dados durante importação
- ✅ **Log Detalhado**: Rastreamento completo de sucessos e erros
- ✅ **Histórico de Importações**: Registro de todas as operações realizadas
- ✅ **Comparação de Versões**: Análise de diferenças entre importações

### 🧹 Tratamento e Qualidade de Dados
- ✅ **Limpeza Automatizada**: Remoção de duplicados com critérios configuráveis
- ✅ **Normalização**: Padronização de texto (maiúsculas, minúsculas, capitalização)
- ✅ **Tratamento de Nulos**: Múltiplas estratégias (preenchimento, remoção, substituição)
- ✅ **Validação de Contatos**: Verificação de formato de e-mails e telefones
- ✅ **Detecção de Outliers**: Identificação estatística via IQR e Z-Score
- ✅ **Normalização Numérica**: Escalonamento de dados para análises
- ✅ **Relatório de Qualidade**: Análise detalhada da integridade dos dados

### 📊 Análise e Relatórios
- ✅ **Dashboard Executivo**: Visão consolidada com KPIs principais
- ✅ **Relatórios Excel**: Documentos multi-abas com dados e estatísticas
- ✅ **Exportação Flexível**: Suporte para Excel, CSV, JSON, TXT
- ✅ **Tabelas Dinâmicas**: Pivot tables para análise cruzada
- ✅ **Estatísticas Descritivas**: Métricas completas (média, mediana, desvio padrão)
- ✅ **Análise de Frequência**: Distribuição de valores e padrões
- ✅ **Dados Temporais**: Análise de tendências por período
- ✅ **Segmentação**: Relatórios por categoria, status, localização

### 🌐 Interface Web (Django)
- **Dashboard Interativo**: Painel de controle com estatísticas em tempo real
- **Painel Administrativo**: Interface Django Admin customizada e profissional
- **Upload Direto**: Importação de arquivos via drag-and-drop ou seleção
- **Filtros Avançados**: Busca e filtração multi-critério
- **Paginação Eficiente**: Navegação otimizada para grandes volumes
- **Design Responsivo**: Compatível com desktop, tablet e mobile
- **Exportação Web**: Download direto de relatórios e dados

### 💻 Interface CLI (Command Line)
- **Menu Interativo**: Navegação intuitiva por funcionalidades
- **Operações em Lote**: Processamento automatizado sem interface gráfica
- **Scripting**: Integrável com automações e pipelines
- **Alta Performance**: Ideal para processamento de grandes volumes

## 📁 Estrutura do Projeto

```
backend_eventos/
├── src/                         # 🐍 Módulos Python Core (CLI)
│   ├── database.py              # Gerenciamento de conexões e ORM SQLite
│   ├── excel_handler.py         # Engine de processamento Excel
│   ├── data_cleaner.py          # Algoritmos de limpeza e validação
│   ├── report_generator.py     # Engine de geração de relatórios
│   └── main.py                 # Interface CLI com menu interativo
│
├── webapp/                      # 🌐 Aplicação Web Django
│   ├── manage.py               # Utilitário de gerenciamento Django
│   ├── core/                   # ⚙️ Configurações do projeto
│   │   ├── settings.py         # Configurações principais
│   │   ├── urls.py            # Roteamento principal
│   │   ├── wsgi.py            # WSGI server interface
│   │   └── asgi.py            # ASGI server interface (async)
│   │
│   └── eventos/                # 📦 App principal de eventos
│       ├── models.py           # Modelos de dados (Evento, Cliente, Participante)
│       ├── views.py            # Controllers e lógica de negócio
│       ├── admin.py            # Customização do Django Admin
│       ├── urls.py             # Rotas da aplicação
│       ├── templates/          # Templates HTML
│       │   └── eventos/        # Templates específicos
│       └── migrations/         # Migrações de banco de dados
│
├── media/                       # 📤 Arquivos enviados e gerados
│   ├── importacoes/            # Excel files importados
│   ├── relatorios/             # Relatórios gerados
│   └── exportacoes/            # Exportações de dados
│
├── staticfiles/                 # 🎨 Arquivos estáticos (CSS, JS, imagens)
│   └── admin/                  # Assets do Django Admin
│
├── data/                        # 💾 Bancos de dados SQLite
│
├── config.py                    # 🔧 Configurações do ambiente
├── requirements.txt             # 📦 Dependências Python
├── pyproject.toml              # 🛠️ Configuração do projeto Python
│
└── 📚 Documentação
    ├── README.md               # Este arquivo
    ├── INICIO_RAPIDO.md        # Guia de início rápido
    ├── DJANGO_GUIDE.md         # Documentação completa do Django
    ├── MELHORIAS.md            # Funcionalidades detalhadas CLI
    └── GUIA_RAPIDO.txt         # Referência rápida de comandos
```

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Instalação Rápida

1. **Clone o repositório**
```bash
git clone https://github.com/JoaoLSouto/backend_eventos.git
cd backend_eventos
```

2. **Configure o ambiente virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure o banco de dados**
```bash
cd webapp
python manage.py migrate
```

5. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

6. **Inicie o servidor**
```bash
python manage.py runserver
```

### 🎉 Pronto! Acesse:
- **Dashboard Principal**: http://localhost:8000/
- **Painel Administrativo**: http://localhost:8000/admin/
- **Documentação da API**: http://localhost:8000/api/docs/ (se configurado)

## 💼 Casos de Uso

### 1. Gestão de Conferências e Seminários
- Controle de múltiplas trilhas e palestras
- Gestão de palestrantes e participantes
- Emissão de certificados
- Análise de audiência por sessão

### 2. Eventos Corporativos
- Gestão de eventos internos (treinamentos, workshops)
- Controle de presença
- Relatórios de participação
- Integração com dados de RH

### 3. Festivais e Shows
- Gestão de diferentes tipos de ingresso (VIP, Pista, Camarote)
- Controle de capacidade e segurança
- Análise de vendas por canal
- Relatórios financeiros

### 4. Eventos Acadêmicos
- Controle de inscrições de estudantes
- Gestão de workshops e minicursos
- Certificação automatizada
- Análise estatística de participação

### 5. Webinars e Eventos Online
- Registro de participantes virtuais
- Rastreamento de presença online
- Integração com plataformas de streaming
- Análise de engajamento

## 🎮 Guia de Uso

### 🌐 Interface Web (Recomendado)

#### Inicialização Rápida (Windows)
```powershell
.\iniciar_django.ps1
```

#### Inicialização Manual
```bash
cd webapp
python manage.py migrate
python manage.py createsuperuser  # Apenas primeira vez
python manage.py runserver
```

**Acesse**: http://localhost:8000/

#### Fluxo de Trabalho Web
1. **Login** → Acesse com suas credenciais
2. **Dashboard** → Visualize estatísticas gerais
3. **Criar Evento** → Configure novo evento
4. **Importar Participantes** → Upload de arquivo Excel
5. **Gerenciar** → Visualize e edite dados
6. **Gerar Relatórios** → Exporte análises

### 💻 Interface CLI (Terminal)

Execute o menu interativo:
```bash
python src/main.py
```

#### Opções do Menu CLI
```
📋 BANCO DE DADOS E EXCEL
[1] Importar Excel → Banco de dados
[2] Visualizar tabelas disponíveis
[3] Consultar dados com filtros
[4] Preview de arquivo Excel

🧹 TRATAMENTO DE DADOS
[11] Limpeza avançada (duplicados, nulos, formatação)
[12] Validação de e-mails e telefones
[13] Remover outliers estatísticos
[14] Normalizar dados numéricos
[15] Relatório de qualidade

📊 RELATÓRIOS E ANÁLISE
[16] Gerar relatório Excel completo
[17] Estatísticas descritivas
[18] Relatório resumido (TXT)
[19] Tabela dinâmica (Pivot)
[20] Análise de frequência

💾 MANIPULAÇÃO
[21] Inserir registro manualmente
[22] Atualizar registro
[23] Deletar registros
[24] Exportar para Excel
[25] Backup de tabela
```

### 📝 Exemplos Práticos

#### Exemplo 1: Importar e Limpar Dados
```bash
# Via Web
1. Login → Dashboard
2. "Importar Excel" → Selecionar arquivo
3. "Limpar Dados" → Selecionar evento
4. Aplicar validações → Salvar

# Via CLI
python src/main.py
→ [1] Importar Excel
→ [11] Limpar dados avançados
→ [7] Aplicar todas as limpezas
```

#### Exemplo 2: Gerar Relatório Completo
```bash
# Via Web
Dashboard → Eventos → Selecionar evento → "Gerar Relatório" → Excel

# Via CLI
python src/main.py
→ [16] Gerar relatório Excel
→ Escolher tabela
→ Relatório salvo em /relatorios/
```

#### Exemplo 3: Análise Estatística
```bash
# Via Web
Dashboard → Estatísticas → Filtrar por período/categoria

# Via CLI
python src/main.py
→ [17] Estatísticas descritivas
→ [19] Tabela dinâmica
→ [20] Análise de frequência
```

## 📦 Dependências e Requisitos

### Dependências Principais
```
Core Framework
├── Django>=5.0.1              # Framework web full-stack
├── djangorestframework        # API REST (opcional)
└── django-import-export>=3.3.5 # Importação/exportação avançada

Data Processing
├── pandas==2.2.0              # Análise e manipulação de dados
├── numpy                      # Operações numéricas e arrays
├── openpyxl==3.1.2           # Processamento Excel (.xlsx)
└── sqlalchemy==2.0.25        # ORM para banco de dados

UI/Frontend
├── django-crispy-forms>=2.1   # Formulários estilizados
├── crispy-bootstrap5>=2025.6  # Bootstrap 5 integration
└── whitenoise>=6.6.0          # Serving de arquivos estáticos

Utilities
├── python-dotenv==1.0.0       # Variáveis de ambiente
└── pillow>=10.2.0             # Processamento de imagens
```

### Requisitos de Sistema
- **Python**: 3.10+
- **Memória RAM**: 2GB mínimo, 4GB recomendado
- **Espaço em Disco**: 500MB para aplicação + espaço para dados
- **Navegador**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

## 🔒 Segurança e Boas Práticas

### Recursos de Segurança
- ✅ **Autenticação Django**: Sistema robusto de login e sessões
- ✅ **CSRF Protection**: Proteção contra Cross-Site Request Forgery
- ✅ **SQL Injection Prevention**: Queries parametrizadas via ORM
- ✅ **XSS Protection**: Sanitização automática de templates
- ✅ **Validação de Dados**: Validadores em modelos e formulários
- ✅ **Controle de Permissões**: Decorators de autenticação

### Recomendações para Produção
1. **Environment Variables**: Use `.env` para credenciais
2. **DEBUG=False**: Desabilite modo debug em produção
3. **HTTPS**: Configure SSL/TLS para conexões seguras
4. **Backup Regular**: Implemente rotina de backup do banco
5. **Logging**: Configure logs para auditoria
6. **Rate Limiting**: Implemente controle de requisições
7. **Database**: Migre para PostgreSQL ou MySQL em produção

## 🌟 Diferenciais Competitivos

### ✨ O que torna este sistema único:

1. **Arquitetura Dual**
   - Interface Web moderna + CLI poderoso
   - Flexibilidade para diferentes perfis de usuário
   - Automação via scripts + interação visual

2. **Data Quality First**
   - Validação em múltiplas camadas
   - Limpeza automatizada com algoritmos avançados
   - Relatórios de qualidade de dados
   - Detecção estatística de anomalias

3. **Escalabilidade**
   - Suporte para milhares de participantes
   - Processamento em batch otimizado
   - Paginação eficiente
   - Cache estratégico

4. **Experiência do Usuário**
   - Interface intuitiva e responsiva
   - Feedback em tempo real
   - Operações em um clique
   - Documentação completa

5. **Modularidade**
   - Componentes independentes e reutilizáveis
   - Fácil extensão de funcionalidades
   - Integração simplificada
   - Manutenção facilitada

6. **Analytics Embarcado**
   - Dashboard com KPIs
   - Relatórios multi-formato
   - Análise estatística avançada
   - Tabelas dinâmicas

## 🎓 Conceitos e Tecnologias Implementados

Este projeto demonstra proficiência em:

**Backend & Frameworks**
- Django MVT Architecture
- ORM e Database Design
- RESTful principles
- Authentication & Authorization

**Data Science & Analytics**
- Data cleaning e preprocessing
- Statistical analysis (outliers, normalization)
- Pandas & NumPy operations
- Data validation techniques

**Software Engineering**
- SOLID principles
- Design Patterns (Repository, Service Layer)
- Clean Code practices
- Modular architecture

**DevOps & Best Practices**
- Environment configuration
- Dependency management
- Version control (Git)
- Documentation

## 📚 Documentação Adicional

Para informações mais detalhadas, consulte:

- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Guia de início rápido e configuração inicial
- **[DJANGO_GUIDE.md](DJANGO_GUIDE.md)** - Documentação completa do Django e web interface
- **[MELHORIAS.md](MELHORIAS.md)** - Detalhamento de funcionalidades CLI e casos de uso
- **[GUIA_RAPIDO.txt](GUIA_RAPIDO.txt)** - Referência rápida de comandos

## 🚀 Roadmap e Melhorias Futuras

### Em Desenvolvimento
- [ ] API REST completa com Django REST Framework
- [ ] Autenticação OAuth2 e JWT
- [ ] WebSockets para notificações em tempo real
- [ ] Dashboard com gráficos interativos (Chart.js/Plotly)

### Planejado
- [ ] Exportação de certificados em PDF
- [ ] Sistema de templates de e-mail
- [ ] Integração com provedores de pagamento
- [ ] App mobile (React Native/Flutter)
- [ ] Machine Learning para previsão de demanda
- [ ] Sistema de CRM integrado
- [ ] Multi-tenancy support
- [ ] Internacionalização (i18n) completa

### Integrações Possíveis
- Google Calendar / Outlook
- Mailchimp / SendGrid
- Stripe / PayPal
- Zoom / Google Meet
- Social Media APIs

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes
- Siga as convenções de código Python (PEP 8)
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Mantenha commits atômicos e bem descritos

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**João Luiz Souto**
- GitHub: [@JoaoLSouto](https://github.com/JoaoLSouto)

## 🙏 Agradecimentos

- Comunidade Django pela excelente documentação
- Pandas development team
- Todos os contribuidores open-source

---

## 📞 Suporte

Para questões, sugestões ou reportar problemas:
- Abra uma [Issue](https://github.com/JoaoLSouto/backend_eventos/issues)
- Entre em contato via GitHub

---

<div align="center">
  
**⭐ Se este projeto foi útil, considere dar uma estrela!**

Desenvolvido com ❤️ usando Django e Python

</div>
