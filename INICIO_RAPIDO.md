# 🚀 GUIA DE INICIALIZAÇÃO RÁPIDA - DJANGO

## Passos para Iniciar o Sistema

### 1️⃣ Instalar Dependências

```bash
# Ative o ambiente virtual se ainda não estiver ativo
.\.venv\Scripts\Activate.ps1

# Instale as dependências Django
pip install Django==5.0.1 django-import-export==3.3.5 django-crispy-forms==2.1 crispy-bootstrap5==2.0.0 pillow==10.2.0 whitenoise==6.6.0
```

### 2️⃣ Configurar Banco de Dados

```bash
# Entre na pasta webapp
cd webapp

# Crie as tabelas no banco de dados
python manage.py migrate
```

### 3️⃣ Criar Usuário Administrador

```bash
# Crie um superusuário para acessar o admin
python manage.py createsuperuser

# Siga as instruções:
# Username: admin (ou seu nome)
# Email: seu@email.com
# Password: ******* (senha segura)
# Password (again): *******
```

### 4️⃣ Iniciar Servidor

```bash
# Inicie o servidor de desenvolvimento
python manage.py runserver

# O servidor estará disponível em:
# http://localhost:8000/
```

### 5️⃣ Acessar Sistema

Abra seu navegador e acesse:

- **Dashboard**: http://localhost:8000/
- **Admin Django**: http://localhost:8000/admin/
  - Username: admin (ou o que você criou)
  - Password: sua senha

## 🎯 Primeiro Uso

### Criar um Evento

1. Acesse http://localhost:8000/admin/
2. Clique em **"Eventos"** → **"Adicionar Evento"**
3. Preencha:
   - Nome do evento
   - Data e horário
   - Local
   - Capacidade máxima
   - Valor do ingresso
4. Clique em **"Salvar"**

### Adicionar Participantes

1. No mesmo formulário do evento, role até **"Participantes"**
2. Clique em **"Adicionar outro Participante"**
3. Preencha os dados:
   - Nome completo
   - E-mail
   - Telefone
   - Tipo (VIP, comum, staff, palestrante)
4. Salve

### Importar do Excel

1. Acesse http://localhost:8000/importar/
2. Clique em **"Selecionar arquivo"**
3. Escolha seu arquivo Excel
4. Clique em **"Importar Dados"**
5. Aguarde o processamento

## 📊 Estrutura do Projeto Completo

```
projeto_evento/
├── src/                    # Módulos Python originais
│   ├── main.py            # Sistema CLI
│   ├── database.py        # Banco SQLite
│   ├── excel_handler.py   # Manipulação Excel
│   ├── data_cleaner.py    # Limpeza de dados
│   └── report_generator.py # Relatórios
├── webapp/                # 🆕 Aplicação Django
│   ├── manage.py
│   ├── core/             # Configurações Django
│   └── eventos/          # App de eventos
│       ├── models.py     # Modelos de dados
│       ├── admin.py      # Admin customizado
│       ├── views.py      # Controllers
│       └── templates/    # Templates HTML
├── data/                 # Bancos de dados
├── relatorios/          # Relatórios gerados
├── media/               # Uploads (novos arquivos)
└── staticfiles/         # Arquivos estáticos

```

## 🎨 Recursos Disponíveis

### No Sistema CLI (src/main.py)
- Menu interativo no terminal
- Importação e exportação
- Limpeza de dados
- Relatórios

### No Django (webapp/)
- Interface web moderna
- Admin visual profissional
- Upload de arquivos
- Geração de relatórios via web
- Dashboard com estatísticas

## 🔑 Comandos Essenciais

```bash
# Criar migração após alterar models.py
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver

# Shell Django (para testes)
python manage.py shell

# Coletar arquivos estáticos (produção)
python manage.py collectstatic
```

## 💡 Dicas

1. **Use o Admin Django** para gerenciamento visual dos dados
2. **Use o CLI** para processamento em lote e automação
3. **Ambos compartilham** os módulos de limpeza e relatórios
4. **Dados ficam em** `data/django_eventos.db`

## 🆘 Problemas Comuns

### Erro: "No module named 'django'"
**Solução**: `pip install Django==5.0.1`

### Erro: "Table doesn't exist"
**Solução**: `python manage.py migrate`

### Erro: "Permission denied"
**Solução**: Crie um superusuário com `python manage.py createsuperuser`

### Porta 8000 em uso
**Solução**: `python manage.py runserver 8080` (use outra porta)

## 📖 Próximos Passos

1. ✅ Explore o Admin Django
2. ✅ Crie alguns eventos de teste
3. ✅ Importe dados do Excel
4. ✅ Gere relatórios
5. ✅ Personalize o sistema

## 🎓 Aprendendo Mais

- Admin: http://localhost:8000/admin/
- Dashboard: http://localhost:8000/
- Importar: http://localhost:8000/importar/
- Estatísticas: http://localhost:8000/estatisticas/

---

**Pronto para começar! 🚀**

Qualquer dúvida, consulte:
- [DJANGO_GUIDE.md](DJANGO_GUIDE.md) - Documentação completa
- [MELHORIAS.md](MELHORIAS.md) - Funcionalidades do sistema
- [README.md](README.md) - Visão geral do projeto
