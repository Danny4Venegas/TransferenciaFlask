import pyodbc
from OpenSSL import SSL
from cryptography.hazmat.backends import default_backend
from flask import Flask, request
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

app = Flask(__name__)

# Establece la conexión a la base de datos
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=server_name;DATABASE=database_name;UID=user_name;PWD=password')
cursor = cnxn.cursor()

# Carga la clave pública del firmante
with open('public_key.pem', 'rb') as key_file:
    public_key = load_pem_public_key(key_file.read(), backend=default_backend())

# Carga el certificado y la clave privada
context = SSL.Context(SSL.TLSv1_2_METHOD)
context.use_privatekey_file('private_key.pem')
context.use_certificate_file('certificate.pem')

# Establece el contexto SSL en la aplicación
app.run(ssl_context=context)

@app.route('/upload', methods=['POST'])
def upload():
    # Obtén el archivo XML firmado del POST
    xml_file = request.files['xml_file']

    # Verifica la firma del archivo XML
    if not public_key.verify(xml_file.signature, xml_file.data, padding.PKCS1v15(), xml_file.hash_algorithm):
        return 'Error: la firma del archivo XML es inválida', 400

    # Almacena el archivo XML en la base de datos
    cursor.execute("INSERT INTO xml_table (xml_data) VALUES (?)", xml_file.data)
    cnxn.commit()

    return 'El archivo XML ha sido almacenado en la base de datos', 200

if __name__ == '__main__':
    app.run(ssl_context='adhoc')