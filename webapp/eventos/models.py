"""
Models para gerenciamento de eventos e participantes
"""

from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone


class Categoria(models.Model):
    """Categoria de eventos"""

    nome = models.CharField("Nome", max_length=100, unique=True)
    descricao = models.TextField("Descrição", blank=True)
    cor = models.CharField("Cor (hex)", max_length=7, default="#007bff", help_text="Ex: #007bff para azul")
    ativo = models.BooleanField("Ativo", default=True)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    """Cadastro único de clientes/pessoas"""

    nome_completo = models.CharField("Nome Completo", max_length=200)
    email = models.EmailField("E-mail", unique=True, validators=[EmailValidator()])
    telefone = models.CharField(
        "Telefone",
        max_length=20,
        blank=True,
        validators=[RegexValidator(regex=r"^\([0-9]{2}\)\s?[0-9]{4,5}-?[0-9]{4}$", message="Formato: (XX) XXXXX-XXXX")],
    )
    cpf = models.CharField(
        "CPF",
        max_length=14,
        blank=True,
        unique=True,
        null=True,
        validators=[
            RegexValidator(regex=r"^[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}$", message="Formato: XXX.XXX.XXX-XX")
        ],
    )
    data_nascimento = models.DateField("Data de Nascimento", null=True, blank=True)
    cidade = models.CharField("Cidade", max_length=100, blank=True)
    estado = models.CharField("Estado", max_length=2, blank=True)
    observacoes = models.TextField("Observações", blank=True)

    # Campos de controle
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["nome_completo"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["cpf"]),
        ]

    def __str__(self):
        return f"{self.nome_completo} ({self.email})"

    @property
    def total_eventos(self):
        """Total de eventos que o cliente participou"""
        return self.participacoes.count()

    @property
    def idade(self):
        """Calcula idade do cliente"""
        if self.data_nascimento:
            hoje = timezone.now().date()
            return (
                hoje.year
                - self.data_nascimento.year
                - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
            )
        return None


class Evento(models.Model):
    """Modelo principal para eventos"""

    STATUS_CHOICES = [
        ("planejamento", "Em Planejamento"),
        ("confirmado", "Confirmado"),
        ("em_andamento", "Em Andamento"),
        ("concluido", "Concluído"),
        ("cancelado", "Cancelado"),
    ]

    nome = models.CharField("Nome do Evento", max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    descricao = models.TextField("Descrição", blank=True)
    data_evento = models.DateTimeField("Data do Evento")
    data_encerramento = models.DateTimeField("Data de Encerramento", null=True, blank=True)
    local = models.CharField("Local", max_length=300)
    cidade = models.CharField("Cidade", max_length=100, blank=True)
    estado = models.CharField("Estado", max_length=2, blank=True)
    capacidade_maxima = models.IntegerField("Capacidade Máxima", default=0)
    valor_ingresso = models.DecimalField("Valor do Ingresso", max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default="planejamento")
    observacoes = models.TextField("Observações", blank=True)

    # Campos de controle
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)
    ativo = models.BooleanField("Ativo", default=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["-data_evento"]
        indexes = [
            models.Index(fields=["data_evento"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.nome} - {self.data_evento.strftime('%d/%m/%Y')}"

    @property
    def vagas_disponiveis(self):
        """Retorna número de vagas disponíveis"""
        total_inscricoes = self.participantes.filter(status="confirmado").count()
        return max(0, self.capacidade_maxima - total_inscricoes)

    @property
    def taxa_ocupacao(self):
        """Retorna percentual de ocupação"""
        if self.capacidade_maxima == 0:
            return 0
        total_inscricoes = self.participantes.filter(status="confirmado").count()
        return (total_inscricoes / self.capacidade_maxima) * 100

    @property
    def esta_lotado(self):
        """Verifica se evento está lotado"""
        return self.vagas_disponiveis == 0


class Participante(models.Model):
    """Ingressos/Participações em eventos - vincula Cliente a Evento"""

    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("confirmado", "Confirmado"),
        ("cancelado", "Cancelado"),
        ("presente", "Presente"),
        ("ausente", "Ausente"),
    ]

    TIPO_CHOICES = [
        ("vip", "VIP"),
        ("comum", "Comum"),
        ("staff", "Staff"),
        ("palestrante", "Palestrante"),
    ]

    # Relações principais
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="participacoes", verbose_name="Cliente", null=True, blank=True
    )
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="participantes", verbose_name="Evento")

    # Dados do ingresso
    tipo_participante = models.CharField("Tipo", max_length=20, choices=TIPO_CHOICES, default="comum")
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default="pendente")
    codigo_ingresso = models.CharField("Código do Ingresso", max_length=50, unique=True, blank=True)

    # Pagamento
    valor_pago = models.DecimalField("Valor Pago", max_digits=10, decimal_places=2, default=0.00)
    forma_pagamento = models.CharField("Forma de Pagamento", max_length=50, blank=True)

    observacoes = models.TextField("Observações", blank=True)

    # Campos de controle
    data_inscricao = models.DateTimeField("Data da Inscrição", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Participante"
        verbose_name_plural = "Participantes"
        ordering = ["-data_inscricao"]
        unique_together = ["evento", "cliente"]  # Um cliente não pode ter 2 ingressos para o mesmo evento
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["data_inscricao"]),
        ]

    def __str__(self):
        return f"{self.cliente.nome_completo} - {self.evento.nome}"

    def save(self, *args, **kwargs):
        # Gerar código de ingresso se não existir
        if not self.codigo_ingresso:
            import uuid

            self.codigo_ingresso = f"ING-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def nome_completo(self):
        """Alias para compatibilidade"""
        return self.cliente.nome_completo

    @property
    def email(self):
        """Alias para compatibilidade"""
        return self.cliente.email

    @property
    def telefone(self):
        """Alias para compatibilidade"""
        return self.cliente.telefone


class ImportacaoExcel(models.Model):
    """Registro de importações de arquivos Excel"""

    STATUS_CHOICES = [
        ("processando", "Processando"),
        ("sucesso", "Sucesso"),
        ("erro", "Erro"),
    ]

    arquivo = models.FileField("Arquivo Excel", upload_to="importacoes/")
    nome_arquivo = models.CharField("Nome do Arquivo", max_length=255)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default="processando")

    total_linhas = models.IntegerField("Total de Linhas", default=0)
    linhas_importadas = models.IntegerField("Linhas Importadas", default=0)
    linhas_com_erro = models.IntegerField("Linhas com Erro", default=0)

    mensagem_erro = models.TextField("Mensagem de Erro", blank=True)
    log_processamento = models.TextField("Log de Processamento", blank=True)

    usuario = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")

    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    processado_em = models.DateTimeField("Processado em", null=True, blank=True)

    class Meta:
        verbose_name = "Importação de Excel"
        verbose_name_plural = "Importações de Excel"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nome_arquivo} - {self.get_status_display()}"


class RelatorioGerado(models.Model):
    """Histórico de relatórios gerados"""

    TIPO_CHOICES = [
        ("excel", "Excel"),
        ("csv", "CSV"),
        ("pdf", "PDF"),
        ("txt", "Texto"),
    ]

    titulo = models.CharField("Título", max_length=200)
    tipo = models.CharField("Tipo", max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField("Descrição", blank=True)
    arquivo = models.FileField("Arquivo", upload_to="relatorios/")

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Evento")

    usuario = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")

    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        verbose_name = "Relatório Gerado"
        verbose_name_plural = "Relatórios Gerados"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"
