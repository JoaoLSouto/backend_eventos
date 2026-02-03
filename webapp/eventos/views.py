"""
Views para o app de eventos
"""

import sys
from pathlib import Path
import json
from datetime import datetime, timedelta

# Adiciona o diretório raiz ao path para importar módulos src
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse, JsonResponse
from django.utils import timezone
from django.db.models import Count, Q, Sum, Prefetch, Max, Min
from django.core.paginator import Paginator
import pandas as pd

from .models import Evento, Participante, Categoria, ImportacaoExcel, RelatorioGerado
from src.data_cleaner import DataCleaner
from src.report_generator import ReportGenerator


def dashboard(request):
    """Dashboard principal"""
    total_eventos = Evento.objects.filter(ativo=True).count()
    total_participantes = Participante.objects.count()
    eventos_proximos = Evento.objects.filter(data_evento__gte=timezone.now(), ativo=True).order_by("data_evento")[:5]

    # Estatísticas
    eventos_por_status = Evento.objects.values("status").annotate(total=Count("id"))
    participantes_por_status = Participante.objects.values("status").annotate(total=Count("id"))

    context = {
        "total_eventos": total_eventos,
        "total_participantes": total_participantes,
        "eventos_proximos": eventos_proximos,
        "eventos_por_status": eventos_por_status,
        "participantes_por_status": participantes_por_status,
    }
    return render(request, "eventos/dashboard.html", context)


def listar_eventos(request):
    """Lista todos os eventos"""
    eventos = Evento.objects.filter(ativo=True).select_related("categoria")

    # Filtros
    status = request.GET.get("status")
    categoria = request.GET.get("categoria")
    busca = request.GET.get("q")

    if status:
        eventos = eventos.filter(status=status)
    if categoria:
        eventos = eventos.filter(categoria_id=categoria)
    if busca:
        eventos = eventos.filter(Q(nome__icontains=busca) | Q(descricao__icontains=busca) | Q(local__icontains=busca))

    categorias = Categoria.objects.filter(ativo=True)

    context = {
        "eventos": eventos,
        "categorias": categorias,
    }
    return render(request, "eventos/listar_eventos.html", context)


def detalhe_evento(request, evento_id):
    """Detalhes de um evento"""
    evento = get_object_or_404(Evento, id=evento_id)
    participantes = evento.participantes.all().select_related("evento")

    # Estatísticas do evento
    stats = {
        "total": participantes.count(),
        "confirmados": participantes.filter(status="confirmado").count(),
        "pendentes": participantes.filter(status="pendente").count(),
        "presentes": participantes.filter(status="presente").count(),
        "por_tipo": participantes.values("tipo_participante").annotate(total=Count("id")),
    }

    context = {
        "evento": evento,
        "participantes": participantes,
        "stats": stats,
    }
    return render(request, "eventos/detalhe_evento.html", context)


@login_required
def importar_excel(request):
    """Importa dados do Excel ou CSV"""
    if request.method == "POST" and request.FILES.get("arquivo"):
        arquivo = request.FILES["arquivo"]

        try:
            # Salvar registro de importação
            importacao = ImportacaoExcel.objects.create(
                arquivo=arquivo, nome_arquivo=arquivo.name, usuario=request.user, status="processando"
            )

            # Ler arquivo (Excel ou CSV)
            arquivo_nome = arquivo.name.lower()
            if arquivo_nome.endswith(".csv"):
                # Tentar diferentes encodings para CSV
                try:
                    df = pd.read_csv(arquivo, encoding="utf-8")
                except UnicodeDecodeError:
                    try:
                        arquivo.seek(0)
                        df = pd.read_csv(arquivo, encoding="latin-1")
                    except:
                        arquivo.seek(0)
                        df = pd.read_csv(arquivo, encoding="cp1252")
            else:
                df = pd.read_excel(arquivo)

            importacao.total_linhas = len(df)
            importacao.save()

            # Processar linhas
            linhas_importadas = 0
            linhas_atualizadas = 0
            linhas_novas = 0
            linhas_com_erro = 0
            log = []

            # Obter ou criar evento padrão para importação
            evento_padrao = request.POST.get("evento_id")
            if evento_padrao:
                try:
                    evento = Evento.objects.get(id=evento_padrao)
                except Evento.DoesNotExist:
                    evento = None
            else:
                evento = None

            # Se não houver evento selecionado, criar um evento padrão
            if not evento:
                evento, _ = Evento.objects.get_or_create(
                    nome="Importação Excel - " + arquivo.name,
                    defaults={
                        "data_evento": timezone.now(),
                        "local": "A definir",
                        "capacidade_maxima": 1000,
                        "status": "planejamento",
                    },
                )

            for index, row in df.iterrows():
                try:
                    # Normalizar nomes das colunas (aceitar maiúsculas ou minúsculas)
                    row_dict = {k.lower(): v for k, v in row.items()}

                    # Extrair dados
                    nome = row_dict.get("nome", row_dict.get("nome_completo", ""))
                    email = row_dict.get("email", "")
                    telefone = str(row_dict.get("telefone", ""))
                    cpf = str(row_dict.get("cpf", ""))
                    cidade = row_dict.get("cidade", "")
                    estado = row_dict.get("estado", "")
                    status = str(row_dict.get("status", "pendente")).lower()

                    # Mapear status
                    status_map = {
                        "confirmado": "confirmado",
                        "pendente": "pendente",
                        "cancelado": "cancelado",
                        "presente": "presente",
                    }
                    status = status_map.get(status, "pendente")

                    # Criar ou buscar Cliente (baseado no email)
                    from eventos.models import Cliente

                    cliente, cliente_created = Cliente.objects.get_or_create(
                        email=email,
                        defaults={
                            "nome_completo": nome,
                            "telefone": telefone if telefone != "nan" else "",
                            "cpf": cpf if cpf and cpf != "nan" else None,
                            "cidade": cidade if cidade and cidade != "nan" else "",
                            "estado": estado if estado and estado != "nan" else "",
                        },
                    )

                    # Se cliente já existe, atualizar dados se novos valores fornecidos
                    if not cliente_created:
                        atualizado = False
                        # Atualizar nome se fornecido e diferente
                        if nome and nome != "nan" and cliente.nome_completo != nome:
                            cliente.nome_completo = nome
                            atualizado = True
                        if telefone and telefone != "nan" and cliente.telefone != telefone:
                            cliente.telefone = telefone
                            atualizado = True
                        if cidade and cidade != "nan" and cliente.cidade != cidade:
                            cliente.cidade = cidade
                            atualizado = True
                        if estado and estado != "nan" and cliente.estado != estado:
                            cliente.estado = estado
                            atualizado = True
                        if atualizado:
                            cliente.save()

                    # Criar ou atualizar participação (ingresso) no evento
                    # update_or_create garante que não haverá duplicatas
                    participante, created = Participante.objects.update_or_create(
                        evento=evento,
                        cliente=cliente,
                        defaults={
                            "tipo_participante": "comum",
                            "status": status,  # Status é sempre atualizado com o do arquivo
                        },
                    )

                    linhas_importadas += 1
                    if created:
                        linhas_novas += 1
                        if cliente_created:
                            log.append(f"✓ Linha {index+1}: {nome} - Novo cliente e ingresso criados (status: {status})")
                        else:
                            log.append(f"✓ Linha {index+1}: {nome} - Novo ingresso criado (status: {status})")
                    else:
                        linhas_atualizadas += 1
                        log.append(f"↻ Linha {index+1}: {nome} - Ingresso atualizado (status: {status})")

                except Exception as e:
                    linhas_com_erro += 1
                    log.append(f"✗ Linha {index+1}: Erro - {str(e)}")

            # Atualizar importação
            importacao.linhas_importadas = linhas_importadas
            importacao.linhas_com_erro = linhas_com_erro
            importacao.status = "sucesso" if linhas_com_erro == 0 else "erro"
            importacao.log_processamento = "\n".join(log)
            importacao.processado_em = timezone.now()
            importacao.save()

            # Mensagem detalhada de sucesso
            if linhas_com_erro == 0:
                messages.success(
                    request,
                    f"✓ Importação concluída com sucesso! "
                    f"Total: {linhas_importadas} registros | "
                    f"Novos: {linhas_novas} | "
                    f"Atualizados: {linhas_atualizadas}",
                )
            else:
                messages.warning(
                    request,
                    f"Importação concluída com avisos. "
                    f"Sucesso: {linhas_importadas} | "
                    f"Novos: {linhas_novas} | "
                    f"Atualizados: {linhas_atualizadas} | "
                    f"Erros: {linhas_com_erro}",
                )

        except Exception as e:
            messages.error(request, f"Erro ao importar: {str(e)}")

        return redirect("dashboard")

    # GET - Mostrar formulário com lista de eventos
    eventos = Evento.objects.filter(ativo=True).order_by("-data_evento")
    return render(request, "eventos/importar_excel.html", {"eventos": eventos})


@login_required
def limpar_dados(request, evento_id):
    """Limpa e trata dados de um evento"""
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == "POST":
        operacao = request.POST.get("operacao")

        # Obter participantes como DataFrame
        participantes = evento.participantes.all().values(
            "id", "nome_completo", "email", "telefone", "status", "tipo_participante"
        )
        df = pd.DataFrame(list(participantes))

        if df.empty:
            messages.warning(request, "Não há dados para limpar.")
            return redirect("detalhe_evento", evento_id=evento_id)

        # Aplicar limpeza
        cleaner = DataCleaner(df)

        if operacao == "remover_duplicados":
            cleaner.remove_duplicates(subset=["email"])
            messages.success(request, "Duplicados removidos!")

        elif operacao == "padronizar_texto":
            cleaner.standardize_text(operation="title")
            messages.success(request, "Texto padronizado!")

        elif operacao == "validar_emails":
            cleaner.validate_email("email")
            messages.success(request, "E-mails validados!")

        # Atualizar dados no banco
        df_limpo = cleaner.get_cleaned_dataframe()
        ids_validos = df_limpo["id"].tolist()

        # Remover participantes inválidos
        Participante.objects.filter(evento=evento).exclude(id__in=ids_validos).delete()

        return redirect("detalhe_evento", evento_id=evento_id)

    return render(request, "eventos/limpar_dados.html", {"evento": evento})


@login_required
def gerar_relatorio(request, evento_id):
    """Gera relatório de um evento"""
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == "POST":
        tipo_relatorio = request.POST.get("tipo")

        # Obter dados
        participantes = evento.participantes.all().values(
            "nome_completo", "email", "telefone", "status", "tipo_participante", "valor_pago", "data_inscricao"
        )
        df = pd.DataFrame(list(participantes))

        if df.empty:
            messages.warning(request, "Não há dados para gerar relatório.")
            return redirect("detalhe_evento", evento_id=evento_id)

        report_gen = ReportGenerator(df, f"evento_{evento.id}")

        # Gerar relatório
        output_path = Path(__file__).parent.parent.parent / "media" / "relatorios"
        output_path.mkdir(parents=True, exist_ok=True)

        if tipo_relatorio == "excel":
            filename = f"{evento.nome.replace(' ', '_')}_relatorio.xlsx"
            file_path = output_path / filename
            report_gen.generate_excel_report(file_path, include_stats=True)

        elif tipo_relatorio == "csv":
            filename = f"{evento.nome.replace(' ', '_')}_relatorio.csv"
            file_path = output_path / filename
            report_gen.generate_csv_report(file_path)

        elif tipo_relatorio == "txt":
            filename = f"{evento.nome.replace(' ', '_')}_relatorio.txt"
            file_path = output_path / filename
            report_gen.generate_summary_report(file_path)

        # Salvar registro do relatório
        RelatorioGerado.objects.create(
            titulo=f"Relatório - {evento.nome}",
            tipo=tipo_relatorio,
            arquivo=f"relatorios/{filename}",
            evento=evento,
            usuario=request.user,
        )

        messages.success(request, "Relatório gerado com sucesso!")

        # Retornar arquivo para download
        if file_path.exists():
            return FileResponse(open(file_path, "rb"), as_attachment=True, filename=filename)

    return render(request, "eventos/gerar_relatorio.html", {"evento": evento})


def estatisticas(request):
    """Página de estatísticas gerais"""
    # Estatísticas gerais
    total_eventos = Evento.objects.count()
    total_participantes = Participante.objects.count()
    total_categorias = Categoria.objects.count()

    # Calcular taxa de ocupação
    eventos_com_vagas = Evento.objects.exclude(capacidade_maxima=0)
    if eventos_com_vagas.exists():
        total_confirmados = Participante.objects.filter(evento__in=eventos_com_vagas, status="confirmado").count()
        total_vagas = sum(e.capacidade_maxima for e in eventos_com_vagas)
        taxa_ocupacao = (total_confirmados / total_vagas * 100) if total_vagas > 0 else 0
    else:
        taxa_ocupacao = 0

    # Eventos por status
    eventos_por_status = Evento.objects.values("status").annotate(total=Count("id"))
    eventos_status_labels = []
    eventos_status_data = []
    status_dict = dict(Evento.STATUS_CHOICES)
    for item in eventos_por_status:
        eventos_status_labels.append(status_dict.get(item["status"], item["status"]))
        eventos_status_data.append(item["total"])

    # Eventos por categoria
    eventos_por_categoria = Evento.objects.values("categoria__nome").annotate(total=Count("id")).order_by("-total")
    categorias_labels = []
    categorias_data = []
    for item in eventos_por_categoria:
        categorias_labels.append(item["categoria__nome"] or "Sem Categoria")
        categorias_data.append(item["total"])

    # Top eventos com maior participação
    top_eventos = (
        Evento.objects.annotate(
            participantes_confirmados=Count("participantes", filter=Q(participantes__status="confirmado"))
        )
        .filter(capacidade_maxima__gt=0)
        .order_by("-participantes_confirmados")[:10]
    )

    context = {
        "total_eventos": total_eventos,
        "total_participantes": total_participantes,
        "total_categorias": total_categorias,
        "taxa_ocupacao": taxa_ocupacao,
        "eventos_status_labels": json.dumps(eventos_status_labels),
        "eventos_status_data": json.dumps(eventos_status_data),
        "categorias_labels": json.dumps(categorias_labels),
        "categorias_data": json.dumps(categorias_data),
        "top_eventos": top_eventos,
    }
    return render(request, "eventos/estatisticas.html", context)


def historico_vendas(request):
    """Histórico de vendas/ingressos com filtros"""
    # Filtros
    evento_id = request.GET.get("evento")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    status = request.GET.get("status")
    
    # Query base
    vendas = Participante.objects.select_related("evento", "evento__categoria", "cliente").order_by("-data_inscricao")
    
    # Aplicar filtros
    if evento_id:
        vendas = vendas.filter(evento_id=evento_id)
    
    if data_inicio:
        vendas = vendas.filter(data_inscricao__gte=data_inicio)
    
    if data_fim:
        vendas = vendas.filter(data_inscricao__lte=data_fim)
    
    if status:
        vendas = vendas.filter(status=status)
    
    # Estatísticas do filtro aplicado
    total_vendas = vendas.count()
    total_receita = vendas.aggregate(total=Sum("valor_pago"))["total"] or 0
    
    # Vendas por status - garantir que todos os status apareçam
    vendas_por_status_query = vendas.values("status").annotate(total=Count("id"))
    status_dict = {
        "pendente": 0,
        "confirmado": 0,
        "cancelado": 0,
        "presente": 0,
    }
    for item in vendas_por_status_query:
        if item["status"] in status_dict:
            status_dict[item["status"]] = item["total"]
    
    vendas_por_status = [
        {"status": "confirmado", "total": status_dict["confirmado"]},
        {"status": "presente", "total": status_dict["presente"]},
        {"status": "pendente", "total": status_dict["pendente"]},
        {"status": "cancelado", "total": status_dict["cancelado"]},
    ]
    
    # Receita por evento (top 10)
    receita_por_evento = (
        vendas.values("evento__nome")
        .annotate(receita=Sum("valor_pago"), quantidade=Count("id"))
        .order_by("-receita")[:10]
    )
    
    # Vendas por dia (últimos 30 dias ou filtro aplicado)
    from django.db.models.functions import TruncDate
    vendas_por_dia = (
        vendas.annotate(dia=TruncDate("data_inscricao"))
        .values("dia")
        .annotate(quantidade=Count("id"), receita=Sum("valor_pago"))
        .order_by("dia")
    )
    
    # Preparar dados para o gráfico de vendas por dia
    dias_labels = []
    dias_quantidade = []
    dias_receita = []
    for item in vendas_por_dia:
        if item["dia"]:
            dias_labels.append(item["dia"].strftime("%d/%m/%Y"))
            dias_quantidade.append(item["quantidade"])
            dias_receita.append(float(item["receita"] or 0))
    
    # Vendas por mês
    from django.db.models.functions import TruncMonth
    vendas_por_mes = (
        vendas.annotate(mes=TruncMonth("data_inscricao"))
        .values("mes")
        .annotate(quantidade=Count("id"), receita=Sum("valor_pago"))
        .order_by("mes")
    )
    
    # Preparar dados para o gráfico de vendas por mês
    meses_labels = []
    meses_quantidade = []
    meses_receita = []
    for item in vendas_por_mes:
        if item["mes"]:
            meses_labels.append(item["mes"].strftime("%m/%Y"))
            meses_quantidade.append(item["quantidade"])
            meses_receita.append(float(item["receita"] or 0))
    
    # Paginação
    paginator = Paginator(vendas, 50)  # 50 vendas por página
    page_number = request.GET.get("page")
    vendas_page = paginator.get_page(page_number)
    
    # Lista de eventos para o filtro
    eventos = Evento.objects.filter(ativo=True).order_by("-data_evento")
    
    context = {
        "vendas": vendas_page,
        "total_vendas": total_vendas,
        "total_receita": total_receita,
        "vendas_por_status": vendas_por_status,
        "receita_por_evento": receita_por_evento,
        "eventos": eventos,
        "evento_selecionado": evento_id,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "status_selecionado": status,
        "dias_labels": json.dumps(dias_labels),
        "dias_quantidade": json.dumps(dias_quantidade),
        "dias_receita": json.dumps(dias_receita),
        "meses_labels": json.dumps(meses_labels),
        "meses_quantidade": json.dumps(meses_quantidade),
        "meses_receita": json.dumps(meses_receita),
    }
    return render(request, "eventos/historico_vendas.html", context)


@login_required
def central_dados(request):
    """Central de Dados - Visão consolidada de tudo"""
    # Estatísticas gerais
    total_eventos = Evento.objects.count()
    total_participantes = Participante.objects.count()
    total_categorias = Categoria.objects.count()
    total_importacoes = ImportacaoExcel.objects.count()

    # Dados de todos os participantes com relacionamentos
    participantes = Participante.objects.select_related("evento", "evento__categoria").all()

    # Filtros
    evento_id = request.GET.get("evento")
    categoria_id = request.GET.get("categoria")
    status = request.GET.get("status")
    busca = request.GET.get("busca")
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")

    if evento_id:
        participantes = participantes.filter(evento_id=evento_id)
    if categoria_id:
        participantes = participantes.filter(evento__categoria_id=categoria_id)
    if status:
        participantes = participantes.filter(status=status)
    if busca:
        participantes = participantes.filter(
            Q(nome_completo__icontains=busca) | Q(email__icontains=busca) | Q(codigo_ingresso__icontains=busca)
        )
    if data_inicio:
        participantes = participantes.filter(data_inscricao__gte=data_inicio)
    if data_fim:
        participantes = participantes.filter(data_inscricao__lte=data_fim)

    # Ordenação
    ordem = request.GET.get("ordem", "-data_inscricao")
    participantes = participantes.order_by(ordem)

    # Paginação
    paginator = Paginator(participantes, 50)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Listas para filtros
    eventos = Evento.objects.all().order_by("nome")
    categorias = Categoria.objects.all().order_by("nome")

    # Estatísticas da visão atual
    stats_atual = {
        "total": participantes.count(),
        "confirmados": participantes.filter(status="confirmado").count(),
        "pendentes": participantes.filter(status="pendente").count(),
        "cancelados": participantes.filter(status="cancelado").count(),
    }

    context = {
        "page_obj": page_obj,
        "eventos": eventos,
        "categorias": categorias,
        "stats_atual": stats_atual,
        "total_eventos": total_eventos,
        "total_participantes": total_participantes,
        "total_categorias": total_categorias,
        "total_importacoes": total_importacoes,
    }
    return render(request, "eventos/central_dados.html", context)


@login_required
def exportar_dados_completo(request):
    """Exporta TODOS os dados em um único arquivo"""
    formato = request.GET.get("formato", "excel")

    # Buscar todos os participantes com relações
    participantes = (
        Participante.objects.select_related("evento", "evento__categoria")
        .all()
        .values(
            "codigo_ingresso",
            "nome_completo",
            "email",
            "telefone",
            "cpf",
            "data_inscricao",
            "status",
            "evento__nome",
            "evento__data_evento",
            "evento__local",
            "evento__categoria__nome",
            "evento__status",
            "observacoes",
        )
    )

    df = pd.DataFrame(list(participantes))

    if df.empty:
        messages.warning(request, "Não há dados para exportar.")
        return redirect("central_dados")

    # Converter datetimes para timezone-naive (remover timezone para Excel)
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    # Renomear colunas
    df.columns = [
        "Código Ingresso",
        "Nome",
        "Email",
        "Telefone",
        "CPF",
        "Data Inscrição",
        "Status Participante",
        "Evento",
        "Data Evento",
        "Local",
        "Categoria",
        "Status Evento",
        "Observações",
    ]

    # Preparar arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if formato == "excel":
        filename = f"dados_completos_{timestamp}.xlsx"
        filepath = Path(__file__).parent.parent.parent / "media" / "exportacoes" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Dados Completos", index=False)

            # Sheet de estatísticas
            stats_df = pd.DataFrame(
                {
                    "Métrica": ["Total de Participantes", "Total de Eventos", "Confirmados", "Pendentes", "Cancelados"],
                    "Valor": [
                        len(df),
                        df["Evento"].nunique(),
                        len(df[df["Status Participante"] == "confirmado"]),
                        len(df[df["Status Participante"] == "pendente"]),
                        len(df[df["Status Participante"] == "cancelado"]),
                    ],
                }
            )
            stats_df.to_excel(writer, sheet_name="Estatísticas", index=False)

        return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)

    elif formato == "csv":
        filename = f"dados_completos_{timestamp}.csv"
        filepath = Path(__file__).parent.parent.parent / "media" / "exportacoes" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(filepath, index=False, encoding="utf-8-sig")

        return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)

    elif formato == "json":
        filename = f"dados_completos_{timestamp}.json"
        response = HttpResponse(
            df.to_json(orient="records", force_ascii=False, indent=2), content_type="application/json"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


@login_required
def historico_importacoes(request):
    """Histórico de todas as importações de arquivos Excel"""
    importacoes = ImportacaoExcel.objects.select_related("usuario").order_by("-criado_em")

    # Paginação
    paginator = Paginator(importacoes, 20)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Estatísticas
    total_importacoes = importacoes.count()
    total_registros = importacoes.aggregate(Sum("linhas_importadas"))["linhas_importadas__sum"] or 0
    primeira_importacao = importacoes.aggregate(Min("criado_em"))["criado_em__min"]
    ultima_importacao = importacoes.aggregate(Max("criado_em"))["criado_em__max"]

    context = {
        "page_obj": page_obj,
        "total_importacoes": total_importacoes,
        "total_registros": total_registros,
        "primeira_importacao": primeira_importacao,
        "ultima_importacao": ultima_importacao,
    }
    return render(request, "eventos/historico_importacoes.html", context)


@login_required
def comparar_importacoes(request):
    """Compara dados entre diferentes importações"""
    importacao1_id = request.GET.get("importacao1")
    importacao2_id = request.GET.get("importacao2")

    importacoes = ImportacaoExcel.objects.all().order_by("-criado_em")

    comparacao = None

    if importacao1_id and importacao2_id:
        imp1 = get_object_or_404(ImportacaoExcel, id=importacao1_id)
        imp2 = get_object_or_404(ImportacaoExcel, id=importacao2_id)

        # Análise comparativa
        comparacao = {
            "importacao1": imp1,
            "importacao2": imp2,
            "diferenca_registros": imp2.linhas_importadas - imp1.linhas_importadas,
            "diferenca_tempo": (imp2.criado_em - imp1.criado_em).days,
        }

    context = {
        "importacoes": importacoes,
        "comparacao": comparacao,
    }
    return render(request, "eventos/comparar_importacoes.html", context)


def listar_participantes(request):
    """Lista todos os participantes do sistema com filtros"""
    # Buscar todos os participantes
    participantes = Participante.objects.select_related("evento", "evento__categoria").all()

    # Estatísticas gerais (sem filtros)
    total_participantes = Participante.objects.count()
    total_confirmados = Participante.objects.filter(status="confirmado").count()
    total_pendentes = Participante.objects.filter(status="pendente").count()
    total_cancelados = Participante.objects.filter(status="cancelado").count()

    # Aplicar filtros
    evento_id = request.GET.get("evento")
    status = request.GET.get("status")
    busca = request.GET.get("busca")

    if evento_id:
        participantes = participantes.filter(evento_id=evento_id)
    if status:
        participantes = participantes.filter(status=status)
    if busca:
        participantes = participantes.filter(
            Q(nome__icontains=busca) | Q(email__icontains=busca) | Q(codigo_ingresso__icontains=busca)
        )

    # Ordenação
    participantes = participantes.order_by("-data_inscricao")

    # Contar participantes filtrados
    participantes_filtrados = participantes.count()

    # Paginação (30 por página)
    paginator = Paginator(participantes, 30)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Lista de eventos para o filtro
    eventos = Evento.objects.all().order_by("nome")

    context = {
        "page_obj": page_obj,
        "total_participantes": total_participantes,
        "total_confirmados": total_confirmados,
        "total_pendentes": total_pendentes,
        "total_cancelados": total_cancelados,
        "participantes_filtrados": participantes_filtrados,
        "eventos": eventos,
    }
    return render(request, "eventos/listar_participantes.html", context)


@login_required
def exportar_participantes(request):
    """Exporta participantes filtrados"""
    formato = request.GET.get("formato", "excel")

    # Aplicar mesmos filtros da listagem
    participantes = Participante.objects.select_related("evento", "evento__categoria").all()

    evento_id = request.GET.get("evento")
    status = request.GET.get("status")

    if evento_id:
        participantes = participantes.filter(evento_id=evento_id)
    if status:
        participantes = participantes.filter(status=status)

    # Buscar dados
    participantes_data = participantes.values(
        "codigo_ingresso",
        "nome",
        "email",
        "telefone",
        "cpf",
        "data_inscricao",
        "status",
        "evento__nome",
        "evento__data_evento",
        "evento__local",
        "evento__categoria__nome",
    )

    df = pd.DataFrame(list(participantes_data))

    if df.empty:
        messages.warning(request, "Não há participantes para exportar com os filtros selecionados.")
        return redirect("listar_participantes")

    # Renomear colunas
    df.columns = [
        "Código Ingresso",
        "Nome",
        "Email",
        "Telefone",
        "CPF",
        "Data Inscrição",
        "Status",
        "Evento",
        "Data Evento",
        "Local",
        "Categoria",
    ]

    # Preparar arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if formato == "excel":
        filename = f"participantes_{timestamp}.xlsx"
        filepath = Path(__file__).parent.parent.parent / "media" / "exportacoes" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        df.to_excel(filepath, index=False, sheet_name="Participantes")

        return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)

    elif formato == "csv":
        filename = f"participantes_{timestamp}.csv"
        filepath = Path(__file__).parent.parent.parent / "media" / "exportacoes" / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(filepath, index=False, encoding="utf-8-sig")

        return FileResponse(open(filepath, "rb"), as_attachment=True, filename=filename)
