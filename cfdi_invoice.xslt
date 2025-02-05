<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:cfdi="http://www.sat.gob.mx/cfd/4" xmlns:tfd="http://www.sat.gob.mx/TimbreFiscalDigital">
    <xsl:template match="/">
        <html>
            <head>
                <title>Representación Impresa del CFDI</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 10px;
                        background-color: #f9f9f9;
                        color: #333;
                        font-size: 10px; /* Tamaño reducido para caber en una hoja */
                    }
                    .container {
                        max-width: 750px;
                        margin: 0 auto;
                        background: #fff;
                        padding: 10px;
                        border-radius: 6px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }
                    h1, h2 {
                        color: #0056b3;
                        text-align: center;
                        font-size: 14px;
                        margin: 10px 0;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 5px;
                        font-size: 9px; /* Tamaño reducido para tablas */
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 5px;
                        text-align: left;
                    }
                    th {
                        background-color: #0056b3;
                        color: #fff;
                        font-weight: bold;
                    }
                    td {
                        background-color: #f9f9f9;
                    }
                    .header {
                        display: flex;
                        justify-content: space-between;
                        margin-bottom: 10px;
                    }
                    .header-left, .header-right {
                        width: 48%;
                        font-size: 9px;
                    }
                    .highlight {
                        font-weight: bold;
                        color: #0056b3;
                    }
                    .footer {
                        display: flex;
                        justify-content: space-between;
                        align-items: flex-end;
                        margin-top: 10px;
                        padding-top: 5px;
                        border-top: 1px solid #ddd;
                    }
                    .footer-left {
                        font-size: 8px;
                        color: #666;
                    }
                    .footer-right {
                        text-align: right;
                        font-size: 10px;
                    }
                    .sellos {
                        font-size: 8px;
                        margin-top: 2px;
                        white-space: pre-wrap; /* Para manejar texto largo */
                    }
                    .info-adicional {
                        display: flex;
                        justify-content: space-between;
                        margin-top: 10px;
                        font-size: 9px;
                    }
                    .info-adicional-left, .info-adicional-right {
                        width: 48%;
                    }
                    .qr-code {
                        text-align: center;
                        margin-top: 10px;
                    }
                    .qr-code img {
                        max-width: 100px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Representación Impresa del CFDI</h1>

                    <!-- Encabezado -->
                    <div class="header">
                        <div class="header-left">
                            <p><span class="highlight">Folio Fiscal:</span> <xsl:value-of select="//cfdi:Comprobante/cfdi:Complemento/tfd:TimbreFiscalDigital/@UUID"/></p>
                            <p><span class="highlight">No. de Serie del CSD:</span> <xsl:value-of select="//cfdi:Comprobante/@NoCertificado"/></p>
                            <p><span class="highlight">Serie:</span> <xsl:value-of select="//cfdi:Comprobante/@Serie"/></p>
                            <p><span class="highlight">Código Postal, Fecha y Hora de Emisión:</span> <xsl:value-of select="//cfdi:Comprobante/@LugarExpedicion"/> <xsl:value-of select="//cfdi:Comprobante/@Fecha"/></p>
                            <p><span class="highlight">Efecto de Comprobante:</span> <xsl:value-of select="//cfdi:Comprobante/@TipoDeComprobante"/></p>
                            <p><span class="highlight">Régimen Fiscal:</span> <xsl:value-of select="//cfdi:Emisor/@RegimenFiscal"/></p>
                            <p><span class="highlight">Exportación:</span> <xsl:value-of select="//cfdi:Comprobante/@Exportacion"/></p>
                        </div>
                        <div class="header-right">
                            <p><span class="highlight">RFC Emisor:</span> <xsl:value-of select="//cfdi:Emisor/@Rfc"/></p>
                            <p><span class="highlight">Nombre Emisor:</span> <xsl:value-of select="//cfdi:Emisor/@Nombre"/></p>
                            <p><span class="highlight">Folio:</span> <xsl:value-of select="//cfdi:Comprobante/@Folio"/></p>
                            <p><span class="highlight">RFC Receptor:</span> <xsl:value-of select="//cfdi:Receptor/@Rfc"/></p>
                            <p><span class="highlight">Nombre Receptor:</span> <xsl:value-of select="//cfdi:Receptor/@Nombre"/></p>
                            <p><span class="highlight">Código Postal Receptor:</span> <xsl:value-of select="//cfdi:Receptor/@DomicilioFiscalReceptor"/></p>
                            <p><span class="highlight">Régimen Fiscal Receptor:</span> <xsl:value-of select="//cfdi:Receptor/@RegimenFiscalReceptor"/></p>
                            <p><span class="highlight">Uso CFDI:</span> <xsl:value-of select="//cfdi:Receptor/@UsoCFDI"/></p>
                        </div>
                    </div>

                    <!-- Conceptos -->
                    <h2>Conceptos</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Descripción</th>
                                <th>Cantidad</th>
                                <th>Unidad</th>
                                <th>Valor Unitario</th>
                                <th>Importe</th>
                                <th>Descuento</th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="//cfdi:Conceptos/cfdi:Concepto">
                                <tr>
                                    <td><xsl:value-of select="@Descripcion"/></td>
                                    <td><xsl:value-of select="@Cantidad"/></td>
                                    <td><xsl:value-of select="@ClaveUnidad"/></td>
                                    <td><xsl:value-of select="@ValorUnitario"/></td>
                                    <td><xsl:value-of select="@Importe"/></td>
                                    <td><xsl:value-of select="@Descuento"/></td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table>

                    <!-- Impuestos -->
                    <h2>Impuestos</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Tipo</th>
                                <th>Base</th>
                                <th>Tasa o Cuota</th>
                                <th>Importe</th>
                            </tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="//cfdi:Comprobante/cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado">

                                <tr>
                                    <td><xsl:value-of select="@Impuesto"/></td>
                                    <td><xsl:value-of select="@Base"/></td>
                                    <td><xsl:value-of select="@TasaOCuota"/></td>
                                    <td><xsl:value-of select="@Importe"/></td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table>

                    <!-- Información Adicional -->
                    <div class="info-adicional">
                        <div class="info-adicional-left">
                            <p><span class="highlight">Moneda:</span> <xsl:value-of select="//cfdi:Comprobante/@Moneda"/></p>
                            <p><span class="highlight">Forma de Pago:</span> <xsl:value-of select="//cfdi:Comprobante/@FormaPago"/></p>
                            <p><span class="highlight">Método de Pago:</span> <xsl:value-of select="//cfdi:Comprobante/@MetodoPago"/></p>
                            <p><span class="highlight">Tipo de Cambio:</span> <xsl:value-of select="//cfdi:Comprobante/@TipoCambio"/></p>
                        </div>
                        <div class="info-adicional-right">
                            <p><span class="highlight">Subtotal:</span> $<xsl:value-of select="//cfdi:Comprobante/@SubTotal"/></p>
                            <p><span class="highlight">Impuestos Trasladados (IVA 16%):</span> $<xsl:value-of select="//cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado/@Importe"/></p>
                            <p><span class="highlight">Total:</span> $<xsl:value-of select="//cfdi:Comprobante/@Total"/></p>
                        </div>
                    </div>

                    <!-- Sellos Digitales -->
                    <div class="sellos">
                        <p><span class="highlight">Sello Digital del CFDI:</span></p>
                        <p><xsl:value-of select="//cfdi:Comprobante/@Sello"/></p>
                        <p><span class="highlight">Sello Digital del SAT:</span></p>
                        <p><xsl:value-of select="//cfdi:Comprobante/cfdi:Complemento/tfd:TimbreFiscalDigital/@SelloSAT"/></p>

                    </div>

                    <!-- Código QR -->
                    <div class="qr-code">
                        <img src="https://storage.googleapis.com/info_club/fotos_choferes_bsf/qr.png" alt="Código QR"/>
                    </div>

                    <!-- Pie de Página -->
                    <div class="footer">
                        <div class="footer-left">
                            <p><strong>Este documento es una representación impresa de un CFDI.</strong></p>
                            <p>Página 1 de 1</p>
                        </div>
                        <div class="footer-right">
                            <p><span class="highlight">RFC del Proveedor de Certificación:</span> <xsl:value-of select="//cfdi:Comprobante/cfdi:Complemento/tfd:TimbreFiscalDigital/@RfcProvCertif"/></p>
                            <p><span class="highlight">No. de Serie del Certificado SAT:</span> <xsl:value-of select="//cfdi:Comprobante/cfdi:Complemento/tfd:TimbreFiscalDigital/@NoCertificadoSAT"/></p>
                            <p><span class="highlight">Fecha y Hora de Certificación:</span> <xsl:value-of select="//cfdi:Comprobante/cfdi:Complemento/tfd:TimbreFiscalDigital/@FechaTimbrado"/></p>
                        </div>
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>