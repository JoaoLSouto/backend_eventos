"""
Configuração do Django Admin para o app eventos
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Categoria, Evento, Participante, ImportacaoExcel, RelatorioGerado, Cliente


# Resources para import/export
class ParticipanteResource(resources.ModelResource):
    class Meta:
        model = Participante
        fields = (
            "id",
            "evento__nome",
            "nome_completo",
            "email",
            "telefone",
            "tipo_participante",
            "status",
            "valor_pago",
            "data_inscricao",
        )
        export_order = fields


class EventoResource(resources.ModelResource):
    class Meta:
        model = Evento
        fields = (
            "id",
            "nome",
            "data_evento",
            "local",
            "cidade",
            "estado",
            "capacidade_maxima",
            "valor_ingresso",
            "status",
        )
        export_order = fields


# Admin Customizado
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "cor_badge", "ativo", "criado_em")
    list_filter = ("ativo", "criado_em")
    search_fields = ("nome", "descricao")
    list_editable = ("ativo",)

    def cor_badge(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px; ' 'border-radius: 3px; color: white;">{}</span>',
            obj.cor,
            obj.nome,
        )

    cor_badge.short_description = "Cor"


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome_completo", "email", "telefone", "cpf", "cidade", "total_eventos_display", "criado_em")
    list_filter = ("criado_em", "cidade", "estado")
    search_fields = ("nome_completo", "email", "telefone", "cpf")
    readonly_fields = ("criado_em", "atualizado_em", "total_eventos_display")
    date_hierarchy = "criado_em"

    fieldsets = (
        ("Informações Pessoais", {"fields": ("nome_completo", "email", "telefone", "cpf", "data_nascimento")}),
        ("Localização", {"fields": ("cidade", "estado")}),
        ("Estatísticas", {"fields": ("total_eventos_display",)}),
        ("Observações", {"fields": ("observacoes",), "classes": ("collapse",)}),
        ("Controle", {"fields": ("criado_em", "atualizado_em"), "classes": ("collapse",)}),
    )

    def total_eventos_display(self, obj):
        total = obj.total_eventos
        return format_html('<strong>{}</strong> evento(s)', total)
    total_eventos_display.short_description = "Total de Eventos"


class ParticipanteInline(admin.TabularInline):
    model = Participante
    extra = 0
    fields = ("cliente", "tipo_participante", "status", "valor_pago")
    readonly_fields = ("codigo_ingresso", "data_inscricao")
    can_delete = True
    autocomplete_fields = ["cliente"]


@admin.register(Evento)
class EventoAdmin(ImportExportModelAdmin):
    resource_class = EventoResource
    list_display = (
        "nome",
        "data_evento",
        "local_completo",
        "status_badge",
        "ocupacao",
        "total_participantes",
        "valor_ingresso",
    )
    list_filter = ("status", "categoria", "data_evento", "cidade", "estado")
    search_fields = ("nome", "descricao", "local", "cidade")
    readonly_fields = ("criado_em", "atualizado_em", "vagas_disponiveis", "esta_lotado")
    date_hierarchy = "data_evento"

    fieldsets = (
        ("Informações Básicas", {"fields": ("nome", "categoria", "descricao", "status")}),
        ("Data e Local", {"fields": ("data_evento", "data_encerramento", "local", "cidade", "estado")}),
        (
            "Capacidade e Valores",
            {"fields": ("capacidade_maxima", "vagas_disponiveis", "esta_lotado", "valor_ingresso")},
        ),
        ("Observações", {"fields": ("observacoes",), "classes": ("collapse",)}), 
        ("Controle", {"fields": ("ativo", "criado_em", "atualizado_em"), "classes": ("collapse",)}),
    )

    inlines = [ParticipanteInline]

    def local_completo(self, obj):
        return f"{obj.local}, {obj.cidade}/{obj.estado}" if obj.cidade else obj.local

    local_completo.short_description = "Local"

    def status_badge(self, obj):
        colors = {
            "planejamento": "#6c757d",
            "confirmado": "#007bff",
            "em_andamento": "#ffc107",
            "concluido": "#28a745",
            "cancelado": "#dc3545",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px; ' 'border-radius: 3px; color: white;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    def ocupacao(self, obj):
        # Calcular percentual diretamente para evitar SafeString
        if obj.capacidade_maxima == 0:
            percentual = 0.0
        else:
            total_inscricoes = obj.participantes.filter(status="confirmado").count()
            percentual = (total_inscricoes / obj.capacidade_maxima) * 100.0

        if percentual >= 90:
            color = "#dc3545"  # vermelho
        elif percentual >= 70:
            color = "#ffc107"  # amarelo
        else:
            color = "#28a745"  # verde

        # Formatar valores ANTES de passar para format_html
        percentual_str = f"{percentual:.1f}"
        
        return format_html(
            '<div style="width: 100px; background-color: #f0f0f0; border-radius: 3px;">'
            '<div style="width: {}%; background-color: {}; padding: 2px; '
            'text-align: center; color: white; border-radius: 3px;">{}%</div>'
            "</div>",
            percentual_str,
            color,
            percentual_str,
        )

    ocupacao.short_description = "Ocupação"

    def total_participantes(self, obj):
        confirmados = obj.participantes.filter(status="confirmado").count()
        total = obj.participantes.count()
        return f"{confirmados}/{total}"

    total_participantes.short_description = "Participantes"

    actions = ["marcar_como_confirmado", "marcar_como_concluido", "exportar_participantes"]

    def marcar_como_confirmado(self, request, queryset):
        updated = queryset.update(status="confirmado")
        self.message_user(request, f"{updated} evento(s) marcado(s) como confirmado(s).")

    marcar_como_confirmado.short_description = "Marcar como Confirmado"

    def marcar_como_concluido(self, request, queryset):
        updated = queryset.update(status="concluido")
        self.message_user(request, f"{updated} evento(s) marcado(s) como concluído(s).")

    marcar_como_concluido.short_description = "Marcar como Concluído"


@admin.register(Participante)
class ParticipanteAdmin(ImportExportModelAdmin):
    resource_class = ParticipanteResource
    list_display = (
        "cliente_nome",
        "cliente_email",
        "cliente_telefone",
        "evento",
        "tipo_badge",
        "status_badge",
        "valor_pago",
        "codigo_ingresso",
    )
    list_filter = ("status", "tipo_participante", "evento", "data_inscricao")
    search_fields = ("cliente__nome_completo", "cliente__email", "cliente__telefone", "cliente__cpf", "codigo_ingresso")
    readonly_fields = ("codigo_ingresso", "data_inscricao", "atualizado_em")
    date_hierarchy = "data_inscricao"

    fieldsets = (
        ("Evento", {"fields": ("evento",)}),
        ("Cliente", {"fields": ("cliente",)}),
        ("Inscrição", {"fields": ("tipo_participante", "status", "codigo_ingresso")}),
        ("Pagamento", {"fields": ("valor_pago", "forma_pagamento")}),
        ("Observações", {"fields": ("observacoes",), "classes": ("collapse",)}),
        ("Controle", {"fields": ("data_inscricao", "atualizado_em"), "classes": ("collapse",)}),
    )

    def cliente_nome(self, obj):
        return obj.cliente.nome_completo
    cliente_nome.short_description = "Nome"
    cliente_nome.admin_order_field = "cliente__nome_completo"

    def cliente_email(self, obj):
        return obj.cliente.email
    cliente_email.short_description = "Email"
    cliente_email.admin_order_field = "cliente__email"

    def cliente_telefone(self, obj):
        return obj.cliente.telefone
    cliente_telefone.short_description = "Telefone"

    def tipo_badge(self, obj):
        colors = {
            "vip": "#ffc107",
            "comum": "#007bff",
            "staff": "#6c757d",
            "palestrante": "#28a745",
        }
        color = colors.get(obj.tipo_participante, "#007bff")
        return format_html(
            '<span style="background-color: {}; padding: 3px 8px; '
            'border-radius: 3px; color: white; font-size: 11px;">{}</span>',
            color,
            obj.get_tipo_participante_display(),
        )

    tipo_badge.short_description = "Tipo"

    def status_badge(self, obj):
        colors = {
            "pendente": "#ffc107",
            "confirmado": "#28a745",
            "cancelado": "#dc3545",
            "presente": "#17a2b8",
            "ausente": "#6c757d",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; padding: 3px 8px; '
            'border-radius: 3px; color: white; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    actions = ["confirmar_inscricao", "marcar_como_presente", "cancelar_inscricao"]

    def confirmar_inscricao(self, request, queryset):
        updated = queryset.update(status="confirmado")
        self.message_user(request, f"{updated} inscrição(ões) confirmada(s).")

    confirmar_inscricao.short_description = "Confirmar Inscrição"

    def marcar_como_presente(self, request, queryset):
        updated = queryset.update(status="presente")
        self.message_user(request, f"{updated} participante(s) marcado(s) como presente(s).")

    marcar_como_presente.short_description = "Marcar como Presente"

    def cancelar_inscricao(self, request, queryset):
        updated = queryset.update(status="cancelado")
        self.message_user(request, f"{updated} inscrição(ões) cancelada(s).")

    cancelar_inscricao.short_description = "Cancelar Inscrição"


@admin.register(ImportacaoExcel)
class ImportacaoExcelAdmin(admin.ModelAdmin):
    list_display = (
        "nome_arquivo",
        "status_badge",
        "total_linhas",
        "linhas_importadas",
        "linhas_com_erro",
        "criado_em",
        "usuario",
    )
    list_filter = ("status", "criado_em")
    search_fields = ("nome_arquivo",)
    readonly_fields = (
        "nome_arquivo",
        "status",
        "total_linhas",
        "linhas_importadas",
        "linhas_com_erro",
        "mensagem_erro",
        "log_processamento",
        "criado_em",
        "processado_em",
        "usuario",
    )

    fieldsets = (
        ("Arquivo", {"fields": ("arquivo", "nome_arquivo")}),
        ("Status", {"fields": ("status", "mensagem_erro")}),
        ("Estatísticas", {"fields": ("total_linhas", "linhas_importadas", "linhas_com_erro")}),
        ("Log", {"fields": ("log_processamento",), "classes": ("collapse",)}),
        ("Controle", {"fields": ("usuario", "criado_em", "processado_em")}),
    )

    def status_badge(self, obj):
        colors = {
            "processando": "#ffc107",
            "sucesso": "#28a745",
            "erro": "#dc3545",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px; ' 'border-radius: 3px; color: white;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"


@admin.register(RelatorioGerado)
class RelatorioGeradoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo_badge", "evento", "arquivo_link", "criado_em", "usuario")
    list_filter = ("tipo", "criado_em", "evento")
    search_fields = ("titulo", "descricao")
    readonly_fields = ("arquivo", "criado_em", "usuario")
    date_hierarchy = "criado_em"

    fieldsets = (
        ("Informações", {"fields": ("titulo", "tipo", "descricao", "evento")}),
        ("Arquivo", {"fields": ("arquivo",)}),
        ("Controle", {"fields": ("usuario", "criado_em")}),
    )

    def tipo_badge(self, obj):
        colors = {
            "excel": "#28a745",
            "csv": "#007bff",
            "pdf": "#dc3545",
            "txt": "#6c757d",
        }
        color = colors.get(obj.tipo, "#6c757d")
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px; ' 'border-radius: 3px; color: white;">{}</span>',
            color,
            obj.get_tipo_display(),
        )

    tipo_badge.short_description = "Tipo"

    def arquivo_link(self, obj):
        if obj.arquivo:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.arquivo.url)
        return "-"

    arquivo_link.short_description = "Arquivo"
