import lxml.etree as ET
from weasyprint import HTML
import os

# Ruta de la plantilla XSLT
XSLT_PATH = os.path.join(os.path.dirname(__file__), "cfdi_invoice.xslt")

# Función para convertir XML a HTML usando XSLT
def convert_xml_to_html(xml_content, xslt_path):
    try:
        xml_doc = ET.fromstring(xml_content)
        xslt_doc = ET.parse(xslt_path)
        transform = ET.XSLT(xslt_doc)
        html_result = transform(xml_doc)
        return str(html_result)
    except Exception as e:
        return f"Error en la conversión XML a HTML: {e}"

# Función para convertir HTML a PDF
def convert_html_to_pdf(html_content, pdf_path):
    try:
        HTML(string=html_content).write_pdf(pdf_path)
        return True
    except Exception as e:
        return f"Error en la conversión HTML a PDF: {e}"

# Función para procesar múltiples archivos XML y generar PDFs
def process_and_generate_pdfs(xml_data_list, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # Asegurar que la carpeta existe
    pdf_paths = []
    results = []

    for i, factura in enumerate(xml_data_list):
        try:
            xml_content = factura.get("XML Content", "")
            if not xml_content:
                raise ValueError("No se encontró el contenido XML en la factura")

            html_content = convert_xml_to_html(xml_content, XSLT_PATH)

            if "Error en la conversión" in html_content:
                raise ValueError(html_content)  # Si hubo error en la conversión

            # Crear nombre seguro para el archivo PDF
            filename = f"factura_{factura.get('UUID', i + 1)}.pdf"
            pdf_path = os.path.join(output_dir, filename)

            result = convert_html_to_pdf(html_content, pdf_path)
            if result is True:
                pdf_paths.append(pdf_path)
                results.append({'filename': filename, 'status': 'success'})
            else:
                results.append({'filename': filename, 'status': 'error', 'error': result})

        except Exception as e:
            results.append({'filename': f"factura_{i + 1}.pdf", 'status': 'error', 'error': str(e)})
    
    return pdf_paths, results
