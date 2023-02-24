import socket
import ssl
import requests
from datetime import datetime
import streamlit as st


# Función para leer los sitios web de un archivo de texto
def leer_webs():
    with open("web.txt", "r") as f:
        return [line.strip() for line in f.readlines()]

# Función para verificar el certificado SSL de un sitio web y si está en línea
def verificar_certificado(url):
    try:
        cert = ssl.get_server_certificate((url, 443))
        x509 = ssl.PEM_cert_to_X509(cert)
        expira = x509.get_notAfter().decode("ascii")
        expira = datetime.strptime(expira, '%Y%m%d%H%M%SZ')
        dias_restantes = (expira - datetime.now()).days
        response = requests.get(f'https://{url}')
        status_code = response.status_code
        return {
            'url': url,
            'expira_en': dias_restantes,
            'status_code': status_code,
            'online': True
        }
    except (ssl.CertificateError, ssl.SSLError, socket.gaierror, requests.exceptions.RequestException):
        return {
            'url': url,
            'expira_en': 'No se pudo verificar',
            'status_code': '-',
            'online': False
        }

if __name__ == '__main__':
    # Crear la aplicación Streamlit
    st.title("Verificación de certificados SSL")
    webs = leer_webs()
    resultados = []
    for web in webs:
        resultados.append(verificar_certificado(web))
    st.table(resultados)
