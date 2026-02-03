"""
URLs do app eventos
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("eventos/", views.listar_eventos, name="listar_eventos"),
    path("eventos/<int:evento_id>/", views.detalhe_evento, name="detalhe_evento"),
    path("participantes/", views.listar_participantes, name="listar_participantes"),
    path("participantes/exportar/", views.exportar_participantes, name="exportar_participantes"),
    path("importar/", views.importar_excel, name="importar_excel"),
    path("eventos/<int:evento_id>/limpar/", views.limpar_dados, name="limpar_dados"),
    path("eventos/<int:evento_id>/relatorio/", views.gerar_relatorio, name="gerar_relatorio"),
    path("estatisticas/", views.estatisticas, name="estatisticas"),
    path("historico-vendas/", views.historico_vendas, name="historico_vendas"),
    # Central de Dados
    path("central-dados/", views.central_dados, name="central_dados"),
    path("central-dados/exportar/", views.exportar_dados_completo, name="exportar_dados_completo"),
    path("importacoes/historico/", views.historico_importacoes, name="historico_importacoes"),
    path("importacoes/comparar/", views.comparar_importacoes, name="comparar_importacoes"),
]
