from flask import Flask, request
import json
import base64
import rsa
import ssl
import socket
import pymongo

app = Flask(__name__)

def get_pubkey_from_database(sender):
  # Crea una conexión a la base de datos
  client = pymongo.MongoClient("mongodb://localhost:27017/bd")
  db = client["key_scrow"]
  pubkey_collection = db["pubkeys"]

  # Realiza una consulta a la colección de claves públicas de la base de datos
  pubkey_record = pubkey_collection.find_one({"sender": sender})
  if pubkey_record:
    # Devuelve la clave pública encontrada en formato PEM
    return pubkey_record['pubkey'].encode()
  else:
    # Si no se encuentra ningún registro, devuelve None
    return None

def save_signed_xml_to_database(xml, signature, verified):
  # Crea una conexión a la base de datos
  client = pymongo.MongoClient("mongodb://localhost:27017/bd")
  db = client["key_scrow"]
  signed_xml_collection = db["signed_xml"]

  # Inserta el documento XML firmado en la colección de documentos XML firmados de la base de datos
  signed_xml_collection.insert_one({"xml": xml, "signature": signature, "verified": verified})

@app.route('/firmar_xml', methods=['POST'])
def sign_xml():
  # Recupera el documento XML y la clave privada del cuerpo de la solicitud en formato JSON
  data = request.get_json()
  xml = data['xml']
  priv_key = data['priv_key']

  # Carga la clave privada desde una cadena en formato PEM
  priv_key = rsa.PrivateKey.load_pkcs1(priv_key)

  # Firma el documento XML con la clave privada
  signature = rsa.sign(xml.encode(), priv_key, 'SHA-256')

  # Codifica la firma en base64
  signature_b64 = base64.b64encode(signature).decode()

  # Devuelve la firma en base64
  return {'signature': signature_b64}, 200

@app.route('/enviar_firmado', methods=['POST'])
def send_signed_xml():
  # Recupera el documento XML y la firma del cuerpo de la solicitud en formato JSON
  data = request.get_json()
  xml = data['xml']
  signature = data['signature']

  # Decodifica la firma en base64
  signature = base64.b64decode(signature)

  # Crea un socket TCP
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Establece una conexión SSL segura
  ssl_sock = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLS)
  ssl_sock.connect(('localhost', 8443))

  # Envía el documento XML y la firma al servidor
  ssl_sock.sendall(json.dumps({'xml': xml, 'signature': signature}).encode())

  # Recibe la respuesta del servidor
  response = json.loads(ssl_sock.recv(4096).decode())

  # Cierra la conexión SSL
  ssl_sock.close()

  return response, 200

@app.route('/recibir_firmado', methods=['POST'])
def receive_signed_xml():
  # Recupera el documento XML y la firma del cuerpo de la solicitud en formato JSON
  data = request.get_json()
  xml = data['xml']
  signature = data['signature']

  # Decodifica la firma en base64
  signature = base64.b64decode(signature)

  # Verifica la firma del documento XML con la clave pública del remitente
  pub_key = get_pubkey_from_database(data['sender'])
  try:
    rsa.verify(xml.encode(), signature, pub_key)
    verified = True
  except rsa.pkcs1.VerificationError:
    verified = False

  # Guarda el documento XML firmado en la base de datos
  save_signed_xml_to_database(xml, signature, verified)

  return {'message': 'El documento XML firmado ha sido recibido y verificado con éxito.'}, 200

@app.route('/key_escrow', methods=['POST'])
def key_escrow():
  # Recupera las claves del cuerpo de la solicitud en formato JSON
  keys = request.get_json()
  pubkey = keys['pubkey']
  privkey = keys['privkey']

  # Crea una conexión a la base de datos de MongoDB
  client = pymongo.MongoClient("mongodb://localhost:27017/bd")
  db = client["key_scrow"]
  key_escrow_collection = db["key_escrow"]

  # Inserta las claves en la colección de key escrow de la base de datos de MongoDB
  key_escrow_collection.insert_one({"pubkey": pubkey, "privkey": privkey})

  return {'message': 'Las claves han sido almacenadas en la depositaria con éxito.'}, 200

if __name__ == '__main__':
  app.run()
