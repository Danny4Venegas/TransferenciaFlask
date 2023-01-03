import rsa
import base64
from flask import Flask, request
from key_scrow import scrow_key

app = Flask(__name__)

# Genera un par de claves criptográficas
(pubkey, privkey) = rsa.newkeys(512)

#scrow_key(pubkey,privkey)


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

@app.route('/')
def principal():
    return "/recibir<br>/enviar"

@app.route('/recibir')
def receive_signed_xml():
    # Firma el documento XML
    xml_document = '<root><apellido>García</apellido><ci>1726264961</ci><ciudad>Quito</ciudad><correoElectronico>andres@gmail.com</correoElectronico><direccion>antonio román n51-113 y josé peñaherrera</direccion><fechaNacimiento>1998-05-24</fechaNacimiento><mensaje>XD</mensaje><nombre>Andrés</nombre><segundoApellido>Cuvi</segundoApellido><segundoNombre>Wladimir</segundoNombre><select>Soltero</select><telefono>+593992542291</telefono></root>'

    signature = sign(xml_document.encode('utf-8'), privkey)

    # Convierte el objeto de tipo bytes a una cadena de texto
    xml_document_str = xml_document

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