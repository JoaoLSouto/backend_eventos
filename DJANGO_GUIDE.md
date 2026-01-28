# 🌐 INTEGRAÇÃO COM DJANGO

Sistema web completo com interface administrativa para manipulação de dados de eventos.

## 🎯 Funcionalidades Django

### 📊 Dashboard Web
- Visão geral de eventos e participantes
- Estatísticas em tempo real
- Ações rápidas
- Gráficos e indicadores

### 🔧 Painel Administrativo Django
- CRUD completo de eventos
- Gerenciamento de participantes
- Categorização de eventos
- Importação/exportação de dados
- Histórico de operações
- Relatórios gerados

### 📥 Importação de Excel
- Upload de arquivos .xlsx/.xls
- Processamento automático
- Validação de dados
- Log detalhado de erros
- Status de importação

### 🧹 Tratamento de Dados
- Limpeza automática via web
- Validação de e-mails/telefones
- Remoção de duplicados
- Integração com módulos existentes

### 📊 Geração de Relatórios
- Relatórios em Excel, CSV, TXT
- Download direto
- Histórico de relatórios
- Filtros personalizados

## 🚀 Como Iniciar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Aplicar Migrações

```bash
cd webapp
python manage.py migrate
```

### 3. Criar Superusuário

```bash
python manage.py createsuperuser
```

Siga as instruções para criar um usuário administrador.

### 4. Iniciar Servidor

```bash
python manage.py runserver
```

### 5. Acessar o Sistema

- **Dashboard**: http://localhost:8000/
- **Admin Django**: http://localhost:8000/admin/

## 📁 Estrutura Django

```
webapp/
├── manage.py              # Utilitário Django
├── core/                  # Configurações do projeto
│   ├── settings.py        # Configurações Django
│   ├── urls.py           # URLs principais
│   ├── wsgi.py           # WSGI config
│   └── asgi.py           # ASGI config
└── eventos/              # App principal
    ├── models.py         # Modelos de dados
    ├── admin.py          # Configuração do admin
    ├── views.py          # Views/Controllers
    ├── urls.py           # URLs do app
    └── templates/        # Templates HTML
        └── eventos/
            ├── base.html
            ├── dashboard.html
            └── ...
```

## 📊 Modelos de Dados

### Categoria
- Nome, descrição, cor
- Status ativo/inativo
- Organização de eventos

### Evento
- Nome, descrição, local
- Data e horário
- Capacidade e valores
- Status (planejamento, confirmado, em andamento, concluído)
- Relacionamento com participantes

### Participante
- Dados pessoais (nome, email, telefone, CPF)
- Tipo (VIP, comum, staff, palestrante)
- Status (pendente, confirmado, presente, ausente)
- Código de ingresso único
- Relacionamento com evento

### ImportacaoExcel
- Histórico de importações
- Status e estatísticas
- Log de processamento
- Usuário responsável

### RelatorioGerado
- Histórico de relatórios
- Tipo (Excel, CSV, PDF, TXT)
- Arquivo para download
- Associação com evento

## 🎨 Interface Administrativa

### Recursos do Django Admin

✅ **Interface Visual Moderna**
- Layout responsivo
- Badges coloridos para status
- Indicadores visuais
- Gráficos de ocupação

✅ **Filtros Avançados**
- Por status, data, categoria
- Busca em múltiplos campos
- Hierarquia de datas

✅ **Ações em Massa**
- Confirmar eventos
- Marcar como presente
- Cancelar inscrições
- Exportar dados

✅ **Import/Export**
- Importar participantes via Excel
- Exportar em múltiplos formatos
- Validação automática

✅ **Inline Editing**
- Editar participantes dentro do evento
- Adicionar registros rapidamente
- Visualização em tabela

## 🔒 Segurança

- Autenticação obrigatória para importação
- CSRF protection
- Validação de formulários
- Permissões por usuário
- Logs de auditoria

## 🎯 Casos de Uso

### Caso 1: Criar Novo Evento
```
1. Acesse /admin/
2. Clique em "Eventos" → "Adicionar Evento"
3. Preencha os dados
4. Adicione participantes inline
5. Salve
```

### Caso 2: Importar Participantes
```
1. Acesse /importar/
2. Selecione arquivo Excel
3. Upload automático
4. Verifique log no admin
```

### Caso 3: Gerar Relatório
```
1. Acesse o evento desejado
2. Clique em "Gerar Relatório"
3. Escolha o formato
4. Download automático
```

### Caso 4: Limpar Dados
```
1. Acesse o evento
2. Clique em "Limpar Dados"
3. Escolha operação
4. Confirme
```

## 🔧 Comandos Úteis

### Criar novas migrações
```bash
python manage.py makemigrations
```

### Aplicar migrações
```bash
python manage.py migrate
```

### Criar superusuário
```bash
python manage.py createsuperuser
```

### Coletar arquivos estáticos
```bash
python manage.py collectstatic
```

### Shell interativo
```bash
python manage.py shell
```

### Ver SQL das migrações
```bash
python manage.py sqlmigrate eventos 0001
```

## 🎨 Personalização

### Customizar Admin
Edite `webapp/eventos/admin.py` para:
- Adicionar campos na listagem
- Criar novos filtros
- Adicionar ações personalizadas
- Modificar layout

### Adicionar Novos Campos
```python
# 1. Adicione em models.py
class Evento(models.Model):
    novo_campo = models.CharField(max_length=100)

# 2. Crie migração
python manage.py makemigrations

# 3. Aplique
python manage.py migrate
```

### Criar Nova View
```python
# Em views.py
def minha_view(request):
    # Sua lógica
    return render(request, 'template.html', context)

# Em urls.py
path('minha-rota/', views.minha_view, name='minha_view')
```

## 📈 Integração com Módulos Existentes

O Django está **totalmente integrado** com os módulos de limpeza e relatórios:

```python
# Em views.py
from src.data_cleaner import DataCleaner
from src.report_generator import ReportGenerator

# Use normalmente
cleaner = DataCleaner(df)
cleaner.remove_duplicates()

report_gen = ReportGenerator(df, "nome")
report_gen.generate_excel_report(path)
```

## 🌐 Deploy em Produção

### Configurações a Alterar

1. **settings.py**:
   - `DEBUG = False`
   - `SECRET_KEY` segura
   - Configurar `ALLOWED_HOSTS`
   - Usar banco PostgreSQL/MySQL

2. **Arquivos Estáticos**:
   ```bash
   python manage.py collectstatic
   ```

3. **Servidor Web**:
   - Gunicorn/uWSGI
   - Nginx como proxy reverso

### Exemplo com Gunicorn
```bash
pip install gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

## 📚 Recursos Adicionais

- [Documentação Django](https://docs.djangoproject.com/)
- [Django Admin Cookbook](https://books.agiliq.com/projects/django-admin-cookbook/)
- [Import-Export Docs](https://django-import-export.readthedocs.io/)

## 🎓 Próximas Melhorias Sugeridas

1. **API REST** com Django REST Framework
2. **Autenticação Social** (Google, Facebook)
3. **Notificações por Email**
4. **Celery** para tarefas assíncronas
5. **Dashboards Interativos** com Chart.js
6. **QR Code** para ingressos
7. **Check-in Mobile**
8. **Certificados Automáticos**

## 💡 Dicas de Performance

- Use `select_related()` para queries
- Implemente cache com Redis
- Otimize queries com `only()` e `defer()`
- Use paginação em listagens grandes
- Configure índices no banco

## 🐛 Troubleshooting

**Problema**: Erro de migração
**Solução**: `python manage.py migrate --fake eventos zero && python manage.py migrate`

**Problema**: Arquivos estáticos não carregam
**Solução**: `python manage.py collectstatic --clear`

**Problema**: Erro de permissão no admin
**Solução**: Verifique se o usuário é superuser

---

## ✨ Sistema Completo!

Agora você tem:
- ✅ Sistema CLI com menu interativo
- ✅ Interface Web com Django
- ✅ Painel Admin profissional
- ✅ Importação de Excel
- ✅ Tratamento de dados avançado
- ✅ Geração de relatórios
- ✅ Integração total entre módulos

**Comece agora mesmo:**
```bash
cd webapp
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Acesse: http://localhost:8000/ 🚀
