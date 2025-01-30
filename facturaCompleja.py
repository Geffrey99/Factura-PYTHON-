# Ejercicio: Generar una Factura Compleja con ReportLab/Platypus
# #EJERCICIO DE FACTURA COMPLEJA PYTHON 
############################################OKOKOKOKOKOKOKOK

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.units import inch

#--------------------------

###...Función para formatear números dde cantidades monetarias-----
def format_currency(amount):
    return f"€ {amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

###..Datos del encabezado de la factura --------------------
company_info = {
    "logo": "okYoOk.png",  
    "name": "DoubleZZ S.A.",
    "address": "Calle Madriles 83",
    "phone": "+34 123 456 789",
    "email": "info@miempresa.com",
    "website": "www.miempresaDoubleZZ.com"
}

client_info = {
    "name": "Spiderman",
    "address": "Avenida Siempre Viva 456",
    "contact": "+34 987 654 321"
}

invoice_info = {
    "number": "001",
    "issue_date": "24/01/2025",
    "due_date": "27/02/2025"
}

###...Los items de productos -- okokok
items = [
    {"name": "Teclado", "description": "Teclado super fino DS", "quantity": 2, "unit_price": 50.00, "discount": 5.00},
    {"name": "Pantalla HD", "description": "Pantalla 40 pulgadas DS", "quantity": 1, "unit_price": 100.00, "discount": 10.00},
    {"name": "Camara", "description": "Camara super 4k DS", "quantity": 1, "unit_price": 300.00, "discount": 0},
    {"name": "Altavoces", "description": "Ultrasonidos", "quantity": 1, "unit_price": 75.00, "discount": 0},
    {"name": "Alexa Amazon", "description": "Ultima generacion Alexa 7.8", "quantity": 1, "unit_price": 171.00, "discount": 15.00},
    {"name": "Auriculares", "description": "Auriculares DS, ultra bien", "quantity": 1, "unit_price": 700.00, "discount": 30.00},

]

#____Creacion del documento pdf --Okokok------
doc = SimpleDocTemplate("factura.pdf", pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
styles = getSampleStyleSheet()
styleN = styles['Normal']

elements = []

#--------- Encabezado de la factura-------------Okokok
def create_header():
    logo = Image(company_info["logo"], 2*inch, 2*inch)
    company_details = Paragraph(f"""
        <b>{company_info["name"]}</b><br/>
        {company_info["address"]}<br/>
        {company_info["phone"]}<br/>
        {company_info["email"]}<br/>
        {company_info["website"]}
    """, styleN)
    
    client_details = Paragraph(f"""
        <b>Cliente</b><br/>
        {client_info["name"]}<br/>
        {client_info["address"]}<br/>
        {client_info["contact"]}
    """, styleN)
    
    invoice_details = Paragraph(f"""
        <b>Factura Nº:</b> {invoice_info["number"]}<br/>
        <b>Fecha de emisión:</b> {invoice_info["issue_date"]}<br/>
        <b>Fecha de vencimiento:</b> {invoice_info["due_date"]}
    """, styleN)
    
    table_data = [[logo, company_details, invoice_details, client_details]]
    table = Table(table_data, colWidths=[2*inch, 2.5*inch, 2.5*inch, 2.5*inch])
    elements.append(table)
    elements.append(Spacer(1, 12))

#----------Detalles de la factura en tabla-------Okokok
def create_invoice_table():
    table_data = [
        ["Nombre del Artículo", "Descripción", "Cantidad", "Precio Unitario", "Descuento", "Subtotal"]
    ]
    
    for item in items:
        subtotal = (item["quantity"] * item["unit_price"]) - item["discount"]
        table_data.append([
            item["name"],
            item["description"],
            item["quantity"],
            format_currency(item["unit_price"]),
            format_currency(item["discount"]),
            format_currency(subtotal)
        ])
    
    table = Table(table_data, colWidths=[100, 200, 50, 75, 75, 75])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))


#----------Cálculos y totales en tabla--------------- 
def create_totals():
    subtotal_general = sum((item["quantity"] * item["unit_price"]) - item["discount"] for item in items)
    descuento_total = sum(item["discount"] for item in items)
    iva = subtotal_general * 0.21  # 21% IVA
    total_a_pagar = subtotal_general - descuento_total + iva
    
    totals_data = [
        ["Subtotal General", format_currency(subtotal_general)],
        ["Descuento Total", format_currency(descuento_total)],
        ["IVA (21%)", format_currency(iva)],
        ["Total a Pagar", format_currency(total_a_pagar)]
    ]
    
    table = Table(totals_data, colWidths=[400, 75])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))




#el pie de paginaaa Okkkkkkkkk para darle mas seriedad
def create_footer(canvas, doc):
    canvas.saveState()
    footer = Paragraph(f"""
        Términos y Condiciones: No se admiten devoluciones ni se devuelve el dinero. DoubleZZ S.A. <br/>
        Información bancaria: ES00 000 000 000 000 000 <br/>
        Página {doc.page}
    """, styleN)
    width, height = A4
    footer.wrapOn(canvas, width, height)
    footer.drawOn(canvas, 15 * mm, 15 * mm)
    canvas.restoreState()

#____Creacion del documento - Okkk
create_header()
create_invoice_table()
create_totals()
doc.build(elements, onFirstPage=create_footer, onLaterPages=create_footer)

print("Documento PDF de factura iss OKK.")

#✔️✔️✔️✔️✔️✔️

