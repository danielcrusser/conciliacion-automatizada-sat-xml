import lxml.etree as ET
from weasyprint import HTML
import os
import tempfile
import streamlit as st

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

# Función para convertir HTML a PDF (con almacenamiento temporal)
def convert_html_to_pdf(html_content, pdf_path):
    try:
        # Usar un archivo temporal para el HTML
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp_html:
            temp_html.write(html_content.encode())
            temp_html.flush()
            
            # Generar el PDF desde el archivo temporal
            HTML(filename=temp_html.name).write_pdf(pdf_path)
        
        return True
    except Exception as e:
        return f"Error en la conversión HTML a PDF: {e}"

# Función para procesar múltiples archivos XML y generar PDFs
def process_and_generate_pdfs(xml_data_list, output_dir, batch_size=6):
    os.makedirs(output_dir, exist_ok=True)
    pdf_paths = []
    results = []
    
    total_batches = (len(xml_data_list) // batch_size) + 1
    progress_bar = st.progress(0)
    
    # Dividir la lista de facturas en lotes
    for i in range(0, len(xml_data_list), batch_size):
        batch = xml_data_list[i:i + batch_size]
        st.write(f"Procesando lote {i // batch_size + 1} de {total_batches}")
        
        for factura in batch:
            try:
                xml_content = factura.get("XML Content", "")
                if not xml_content:
                    raise ValueError("No se encontró el contenido XML en la factura")
                
                # Convertir XML a HTML
                html_content = convert_xml_to_html(xml_content, XSLT_PATH)
                if "Error en la conversión" in html_content:
                    raise ValueError(html_content)
                
                # Crear nombre seguro para el archivo PDF
                uuid = factura.get("UUID", f"factura_{i + 1}")
                filename = f"{uuid}.pdf"
                pdf_path = os.path.join(output_dir, filename)
                
                # Convertir HTML a PDF
                result = convert_html_to_pdf(html_content, pdf_path)
                if result is True:
                    pdf_paths.append(pdf_path)
                    results.append({'filename': filename, 'status': 'success'})
                else:
                    results.append({'filename': filename, 'status': 'error', 'error': result})
            
            except Exception as e:
                results.append({'filename': f"factura_{i + 1}.pdf", 'status': 'error', 'error': str(e)})
        
        # Actualizar la barra de progreso
        progress = (i + len(batch)) / len(xml_data_list)
        progress_bar.progress(progress)
    
    return pdf_paths, results