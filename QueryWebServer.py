from flask_pymongo import PyMongo
from flask import Flask


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'bd_consolidada'
app.config['MONGO_COLLECTION'] = 'coleccion_prueba'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/db_cris'
mongo = PyMongo(app)

def insertarDatos(datos):
    mongo.db.coleccion_prueba.insert_one(datos)


def mostrarDatos():
    # Realiza una consulta para obtener todos los documentos de la colección
    cursor = mongo.db.coleccion_prueba.find()

    # Recorre el cursor y muestra los datos obtenidos
    for documento in cursor:
        print(documento)




data = {
    'id': "1718043050",
    'nombre': 'Danny',
     'apellido': 'Venegas',
     'telefono':  '+593978762244'
}

#insertarDatos(data)

mostrarDatos()