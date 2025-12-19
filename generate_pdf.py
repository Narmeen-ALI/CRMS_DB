

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

def create_pdf_report(report_data, evidence_list=None, suspects_list=None, officers_list=None, filename=None):
    """
    Generate comprehensive PDF report with all related data
    
    Args:
        report_data: Main report dictionary
        evidence_list: List of evidence items
        suspects_list: List of suspects
        officers_list: List of officers handling the case
        filename: PDF filename (optional)
    """
    

    if not filename:
        filename = f"report_{report_data['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"


    pdf = SimpleDocTemplate(filename, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#8B0000'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    section_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#8B0000'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    


    title = Paragraph("CRIME REPORT MANAGEMENT SYSTEM", title_style)
    elements.append(title)
    
    subtitle = Paragraph(f"<para align=center>Official Crime Report - Case #{report_data['id']}</para>", styles['Heading3'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.3*inch))
    
    section_title = Paragraph("CASE INFORMATION", section_style)
    elements.append(section_title)
    
    report_table_data = [
        ['Field', 'Details'],
        ['Report ID:', f"#{report_data['id']}"],
        ['Filed Date:', report_data.get('created_at', 'N/A')],
        ['Status:', report_data['status']],
        ['Crime Type:', report_data['crime']],
        ['Location:', report_data['location']],
        ['Reporter/Victim:', report_data['reporter']],
        ['Suspect:', report_data['suspect']],
    ]
    
    if report_data.get('notes'):
        report_table_data.append(['Notes:', report_data['notes']])
    
    report_table = Table(report_table_data, colWidths=[2*inch, 4.5*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#F5F5F5')),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 1), (0, -1), colors.HexColor('#333333')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elements.append(report_table)
    elements.append(Spacer(1, 0.3*inch))
    
    if suspects_list and len(suspects_list) > 0:
        section_title = Paragraph("SUSPECTS INVOLVED", section_style)
        elements.append(section_title)
        
        suspect_table_data = [['Name', 'Alias', 'Age', 'Status']]
        
        for suspect in suspects_list:
            suspect_table_data.append([
                suspect.get('full_name', 'N/A'),
                suspect.get('alias', 'N/A') or 'N/A',
                str(suspect.get('age', 'Unknown')),
                suspect.get('suspect_status', 'Unknown')
            ])
        
        suspect_table = Table(suspect_table_data, colWidths=[2*inch, 1.5*inch, 1*inch, 2*inch])
        suspect_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
        ]))
        
        elements.append(suspect_table)
        elements.append(Spacer(1, 0.3*inch))
    
    
    if officers_list and len(officers_list) > 0:
        section_title = Paragraph("OFFICERS HANDLING CASE", section_style)
        elements.append(section_title)
        
        officer_table_data = [['Badge #', 'Name', 'Rank', 'Department']]
        
        for officer in officers_list:
            officer_table_data.append([
                officer.get('badge_number', 'N/A'),
                officer.get('full_name', 'N/A'),
                officer.get('officer_rank', 'N/A'),
                officer.get('department', 'N/A')
            ])
        
        officer_table = Table(officer_table_data, colWidths=[1.2*inch, 2*inch, 1.5*inch, 1.8*inch])
        officer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
        ]))
        
        elements.append(officer_table)
        elements.append(Spacer(1, 0.3*inch))
    
    if evidence_list and len(evidence_list) > 0:
        section_title = Paragraph("EVIDENCE COLLECTED", section_style)
        elements.append(section_title)
        
        evidence_table_data = [['Type', 'Description', 'Collected By', 'Date']]
        
        for evidence in evidence_list:
            desc = evidence.get('description', 'N/A')
            if len(desc) > 60:
                desc = desc[:60] + '...'
            
            evidence_table_data.append([
                evidence.get('evidence_type', 'N/A'),
                desc,
                evidence.get('collected_by', 'Unknown') or 'Unknown',
                evidence.get('collection_date', 'N/A') or 'N/A'
            ])
        
        evidence_table = Table(evidence_table_data, colWidths=[1.2*inch, 2.5*inch, 1.5*inch, 1.3*inch])
        evidence_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
        ]))
        
        elements.append(evidence_table)
        elements.append(Spacer(1, 0.3*inch))
    
    
    elements.append(Spacer(1, 0.2*inch))
    
    footer_text = f"""<para align=center>
    <i>This is an official computer-generated document.<br/>
    Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
    Crime Report Management System - Confidential</i>
    </para>"""
    footer = Paragraph(footer_text, normal_style)
    elements.append(footer)
    
    pdf.build(elements)
    
    print(f" Enhanced PDF Generated: {filename}")
    return filename