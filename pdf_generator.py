# pdf_generator.py - Geração de relatórios em PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io

def gerar_pdf_metas(metas, mes, ano):
    """Gera PDF com relatório de metas"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo customizado para título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulo
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#4a5568'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    # Cabeçalho
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    
    titulo = Paragraph(f"Relatório de Metas e Comissões", title_style)
    subtitulo = Paragraph(f"Período: {meses[mes-1]}/{ano}", subtitle_style)
    data_emissao = Paragraph(f"Emitido em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", 
                             styles['Normal'])
    
    elements.append(titulo)
    elements.append(subtitulo)
    elements.append(data_emissao)
    elements.append(Spacer(1, 0.5*cm))
    
    if not metas:
        sem_dados = Paragraph("Nenhuma meta encontrada para este período.", styles['Normal'])
        elements.append(sem_dados)
    else:
        # Calcular totais
        total_meta = sum(m.valor_meta for m in metas)
        total_receita = sum(m.receita_alcancada for m in metas)
        total_comissao = sum(m.comissao_total for m in metas)
        
        # Resumo
        resumo_data = [
            ['Resumo do Período', '', '', ''],
            ['Total de Vendedores', 'Meta Total', 'Receita Total', 'Comissão Total'],
            [str(len(metas)), f'R$ {total_meta:,.2f}', f'R$ {total_receita:,.2f}', f'R$ {total_comissao:,.2f}']
        ]
        
        resumo_table = Table(resumo_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e2e8f0')),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
            ('SPAN', (0, 0), (-1, 0)),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 2), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ]))
        
        elements.append(resumo_table)
        elements.append(Spacer(1, 1*cm))
        
        # Tabela de detalhes
        detalhes_titulo = Paragraph("Detalhamento por Vendedor", 
                                    ParagraphStyle('DetailTitle', parent=styles['Heading2'],
                                                 fontSize=14, spaceAfter=10))
        elements.append(detalhes_titulo)
        
        # Cabeçalho da tabela
        table_data = [
            ['Vendedor', 'Meta', 'Receita', 'Alcance', 'Comissão', 'Status']
        ]
        
        # Dados
        for meta in metas:
            emoji = get_emoji_alcance(meta.percentual_alcance)
            table_data.append([
                meta.vendedor.nome,
                f'R$ {meta.valor_meta:,.2f}',
                f'R$ {meta.receita_alcancada:,.2f}',
                f'{emoji} {meta.percentual_alcance:.1f}%',
                f'R$ {meta.comissao_total:,.2f}',
                meta.status_comissao
            ])
        
        detail_table = Table(table_data, colWidths=[5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2*cm])
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ]))
        
        # Colorir linha baseado no status
        for i, meta in enumerate(metas, start=1):
            if meta.status_comissao == 'Pago':
                detail_table.setStyle(TableStyle([
                    ('BACKGROUND', (5, i), (5, i), colors.HexColor('#e6fffa'))
                ]))
            elif meta.status_comissao == 'Aprovado':
                detail_table.setStyle(TableStyle([
                    ('BACKGROUND', (5, i), (5, i), colors.HexColor('#f0fff4'))
                ]))
        
        elements.append(detail_table)
        
        # Legenda
        elements.append(Spacer(1, 0.5*cm))
        legenda = Paragraph(
            "<b>Legenda:</b> 🔴 0-50% | 🟡 51-75% | 🔵 76-100% | 🟢 101-125% | 🟢✨ >125%",
            styles['Normal']
        )
        elements.append(legenda)
    
    # Rodapé
    elements.append(Spacer(1, 1*cm))
    rodape = Paragraph(
        "Sistema de Gestão de Metas e Comissões © 2025",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                      textColor=colors.grey, alignment=TA_CENTER)
    )
    elements.append(rodape)
    
    # Gerar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def get_emoji_alcance(percentual):
    """Retorna emoji baseado no percentual"""
    if percentual < 50:
        return '🔴'
    elif percentual < 75:
        return '🟡'
    elif percentual < 100:
        return '🔵'
    elif percentual < 125:
        return '🟢'
    else:
        return '🟢'  # Em PDF não funciona bem com múltiplos emojis

def gerar_pdf_dashboard(resumo_global, vendedores):
    """Gera PDF com relatório do dashboard"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    titulo = Paragraph("Dashboard - Visão Geral", title_style)
    data_emissao = Paragraph(
        f"Emitido em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", 
        styles['Normal']
    )
    
    elements.append(titulo)
    elements.append(data_emissao)
    elements.append(Spacer(1, 0.5*cm))
    
    # Resumo Geral
    resumo_data = [
        ['Indicadores Gerais', '', '', ''],
        ['Total Vendedores', 'Receita Total', 'Meta Total', 'Comissão Total'],
        [
            str(resumo_global.get('total_vendedores', 0)),
            f"R$ {resumo_global.get('receita_total', 0):,.2f}",
            f"R$ {resumo_global.get('meta_total', 0):,.2f}",
            f"R$ {resumo_global.get('comissao_total', 0):,.2f}"
        ]
    ]
    
    resumo_table = Table(resumo_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    resumo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e2e8f0')),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ('SPAN', (0, 0), (-1, 0)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(resumo_table)
    elements.append(Spacer(1, 1*cm))
    
    # Ranking
    if vendedores:
        ranking_titulo = Paragraph("Top Vendedores", 
                                  ParagraphStyle('RankTitle', parent=styles['Heading2'],
                                               fontSize=14, spaceAfter=10))
        elements.append(ranking_titulo)
        
        ranking_data = [['Posição', 'Vendedor', 'Receita', 'Meta', 'Alcance', 'Comissão']]
        
        for i, v in enumerate(vendedores[:10], 1):  # Top 10
            emoji_posicao = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else f'{i}°'
            ranking_data.append([
                emoji_posicao,
                v['nome'],
                f"R$ {v['receita']:,.2f}",
                f"R$ {v['meta']:,.2f}",
                f"{v['percentual']:.1f}%",
                f"R$ {v['comissao']:,.2f}"
            ])
        
        ranking_table = Table(ranking_data, colWidths=[2*cm, 5*cm, 2.5*cm, 2.5*cm, 2*cm, 2.5*cm])
        ranking_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a5568')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ]))
        
        # Destacar top 3
        for i in range(1, min(4, len(vendedores) + 1)):
            ranking_table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (0, i), colors.HexColor('#fff5f5'))
            ]))
        
        elements.append(ranking_table)
    
    # Rodapé
    elements.append(Spacer(1, 1*cm))
    rodape = Paragraph(
        "Sistema de Gestão de Metas e Comissões © 2025",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, 
                      textColor=colors.grey, alignment=TA_CENTER)
    )
    elements.append(rodape)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
