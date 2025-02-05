import streamlit as st
import pandas as pd
import os
import zipfile
import io
from pdf_generator import process_and_generate_pdfs  # Importar la función de generación de PDFs
import xml.etree.ElementTree as ET

# Definir la carpeta de salida de PDFs
OUTPUT_DIR = "output_pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Título de la aplicación
st.title("Conciliación Automatizada de Facturas XML Mensual")

# Función para extraer datos clave del XML
def extract_data_from_xml(file_content, tipo_factura):
    try:
        root = ET.fromstring(file_content)
        namespaces = {'cfdi': 'http://www.sat.gob.mx/cfd/4', 'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'}
        folio = root.attrib.get('Folio', '')
        fecha = root.attrib.get('Fecha', '')
        tipo_comprobante = root.attrib.get('TipoDeComprobante', '')
        uuid = root.find('.//tfd:TimbreFiscalDigital', namespaces).attrib.get('UUID', '')

        emisor = root.find('.//cfdi:Emisor', namespaces)
        rfc_emisor = emisor.attrib.get('Rfc', '')
        nombre_emisor = emisor.attrib.get('Nombre', '')

        receptor = root.find('.//cfdi:Receptor', namespaces)
        rfc_receptor = receptor.attrib.get('Rfc', '')
        nombre_receptor = receptor.attrib.get('Nombre', '')

        subtotal = round(float(root.attrib.get('SubTotal', 0)), 2)
        descuento = round(float(root.attrib.get('Descuento', 0)), 2) if root.attrib.get('Descuento') else 0
        importe = round(float(root.attrib.get('Total', 0)), 2)

        impuestos = root.find('.//cfdi:Impuestos', namespaces)
        iva_traslado = 0
        if impuestos is not None:
            for traslado in impuestos.findall('.//cfdi:Traslado', namespaces):
                if traslado.attrib.get('Impuesto') == '002':
                    iva_traslado += round(float(traslado.attrib.get('Importe', 0)), 2)

        return {
            "Tipo Factura": tipo_factura,
            "Folio": folio,
            "Fecha": fecha,
            "Tipo de Comprobante": tipo_comprobante,
            "UUID": uuid,
            "RFC Emisor": rfc_emisor,
            "Nombre Emisor": nombre_emisor,
            "RFC Receptor": rfc_receptor,
            "Nombre Receptor": nombre_receptor,
            "Subtotal": subtotal,
            "Descuento": descuento,
            "IVA": iva_traslado,
            "Importe": importe,
            "XML Content": file_content  # Se agrega el contenido original del XML
        }
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        return None

# Cargar archivos XML Emitidos y Recibidos
uploaded_emitidas = st.file_uploader("Carga las facturas ---> EMITIDAS", type=["xml"], accept_multiple_files=True)
uploaded_recibidas = st.file_uploader("Carga las facturas ---> RECIBIDAS", type=["xml"], accept_multiple_files=True)

# Procesar archivos XML Emitidos y Recibidos
data_emitidas = []
if uploaded_emitidas:
    for file in uploaded_emitidas:
        file_content = file.read().decode('utf-8')
        extracted_data = extract_data_from_xml(file_content, "Emitida")
        if extracted_data:
            data_emitidas.append(extracted_data)

data_recibidas = []
if uploaded_recibidas:
    for file in uploaded_recibidas:
        file_content = file.read().decode('utf-8')
        extracted_data = extract_data_from_xml(file_content, "Recibida")
        if extracted_data:
            data_recibidas.append(extracted_data)

# Calcular totales
def calcular_totales(data):
    subtotal = round(sum(item["Subtotal"] for item in data), 2)
    descuento = round(sum(item["Descuento"] for item in data), 2)
    iva = round(sum(item["IVA"] for item in data), 2)
    importe = round(sum(item["Importe"] for item in data), 2)
    return {
        "Subtotal": subtotal,
        "Descuento": descuento,
        "IVA": iva,
        "Importe": importe
    }

# Conteo de facturas
if uploaded_emitidas:
    st.write(f"📂 Facturas emitidas cargadas: **{len(uploaded_emitidas)}**")
if uploaded_recibidas:
    st.write(f"📂 Facturas recibidas cargadas: **{len(uploaded_recibidas)}**")

# Mostrar resultados
if data_emitidas or data_recibidas:
    totales_emitidas = calcular_totales(data_emitidas)
    totales_recibidas = calcular_totales(data_recibidas)

    diferencia = {
        "Subtotal": totales_emitidas["Subtotal"] - totales_recibidas["Subtotal"],
        "Descuento": totales_emitidas["Descuento"] - totales_recibidas["Descuento"],
        "IVA": totales_emitidas["IVA"] - totales_recibidas["IVA"],
        "Importe": totales_emitidas["Importe"] - totales_recibidas["Importe"]
    }

    consolidado = {
        "Concepto": ["Subtotal", "Descuento", "IVA", "Importe"],
        "Emitidas": list(totales_emitidas.values()),
        "Recibidas": list(totales_recibidas.values()),
        "Diferencia": list(diferencia.values())
    }

    df_consolidado = pd.DataFrame(consolidado)

    st.subheader("Resumen Consolidado")
    st.dataframe(df_consolidado)

    # Crear un DataFrame combinado de Emitidas y Recibidas para mostrar y exportar
    df_todas_facturas = pd.DataFrame(data_emitidas + data_recibidas)
    df_todas_facturas_pdf = df_todas_facturas.copy()  # Copia para generación de PDFs

    # Eliminar la columna "XML Content" SOLO para la visualización y exportación
    if "XML Content" in df_todas_facturas.columns:
        df_todas_facturas = df_todas_facturas.drop(columns=["XML Content"])

    # Descargar reporte consolidado en Excel
    st.subheader("Descargar Reporte Consolidado")
    if not df_todas_facturas.empty:
        output_file = "reporte_consolidado.xlsx"

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df_todas_facturas.to_excel(writer, sheet_name="Facturas", index=False)
            if not df_consolidado.empty:
                df_consolidado.to_excel(writer, sheet_name="Resumen Consolidado", index=False)

        with open(output_file, "rb") as f:
            st.download_button(
                label="Descargar Excel",
                data=f,
                file_name=output_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("No hay datos suficientes para generar el reporte.")

    # Generar PDFs desde XML
    st.subheader("Generar PDFs desde XML")
    if st.button("Generar PDFs"):
        with st.spinner("Generando PDFs..."):
            pdf_data = df_todas_facturas_pdf.to_dict(orient="records")
            pdf_paths, results = process_and_generate_pdfs(pdf_data, OUTPUT_DIR)

            for result in results:
                if result['status'] == 'success':
                    st.success(f"Archivo generado: {result['filename']}")
                else:
                    st.error(f"Error en {result['filename']}: {result['error']}")

            if pdf_paths:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for pdf_path in pdf_paths:
                        zip_file.write(pdf_path, os.path.basename(pdf_path))
                
                zip_buffer.seek(0)
                st.download_button(
                    label="Descargar Todos los PDFs (.zip)",
                    data=zip_buffer,
                    file_name="facturas.zip",
                    mime="application/zip"
                )
            else:
                st.warning("No se generaron PDFs.")
