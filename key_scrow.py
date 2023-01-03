import pymongo


# Crea una conexión al servidor de Mongo en localhost en el puerto 27017
client = pymongo.MongoClient('mongodb://localhost:27017/')

db = client.mi_base_de_datos  # Selecciona la base de datos a utilizar

keys_collection = db.keys  # Selecciona la colección que almacenará las claves

def scrow_key(pubkey, privkey):
    # Convierte las claves a cadenas de texto en formato pkcs1 para poder almacenarlas en la base de datos
    pubkey_str = pubkey.save_pkcs1().decode('utf-8')
    privkey_str = privkey.save_pkcs1().decode('utf-8')

    # Crea un documento de la clave en la colección
    key_document = {
        'pubkey': pubkey_str,
        'privkey': privkey_str
    }
    keys_collection.insert_one(key_document)  # Inserta el documento en la colección


