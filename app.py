import rsa
import base64
from flask import Flask, request

app = Flask(__name__)

# Genera un par de claves criptográficas
(pubkey, privkey) = rsa.newkeys(512)


# Función de firma digital
def sign(message, privkey):
    signature = rsa.sign(message, privkey, 'SHA-256')
    return signature


# Función de verificación de firma digital
def verify(message, signature, pubkey):
    try:
        rsa.verify(message, signature, pubkey)
        return True
    except rsa.pkcs1.VerificationError:
        return False


@app.route('/enviar', methods=['POST'])
def send_signed_xml():
    # Carga la clave pública desde la cadena de texto
    pubkey = rsa.PublicKey.load_pkcs1(base64.b64decode(request.json['pubkey']))

    # Obtiene el documento XML y la firma digital del cliente
    xml_document = request.json['xml_document']
    signature = base64.b64decode(request.json['signature'])

    # Verifica la firma digital del documento XML recibido
    if verify(xml_document.encode('utf-8'), signature, pubkey):
        print("La firma digital es válida.")
        return {'message': 'La firma digital es válida.'}, 200
    else:
        print("La firma digital no es válida.")
        return {'message': 'La firma digital no es válida.'}, 400


@app.route('/recibir')
def receive_signed_xml():
    # Firma el documento XML
    xml_document = b'<xml>Mi documento XML</xml>'
    signature = sign(xml_document, privkey)

    # Convierte el objeto de tipo bytes a una cadena de texto
    xml_document_str = xml_document.decode('utf-8')

    # Encode the signature and public key in base64
    encoded_signature = base64.b64encode(signature).decode('utf-8')
    encoded_pubkey = base64.b64encode(pubkey.save_pkcs1()).decode('utf-8')

    # Devuelve el documento XML firmado y la clave pública al cliente
    return {
        'xml_document': xml_document_str,
        'signature': encoded_signature,
        'pubkey': encoded_pubkey
    }


if __name__ == '__main__':
    app.run()