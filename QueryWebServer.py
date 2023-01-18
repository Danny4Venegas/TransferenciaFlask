from flask_pymongo import PyMongo
import pyodbc
from dicttoxml import dicttoxml
from flask import Flask

#Se debe cambiar la conexión a una base de datos SQL
app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'bd_consolidada'
app.config['MONGO_COLLECTION'] = 'coleccion_prueba'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/db_cris'
mongo = PyMongo(app)

#Función de prueba para insertar datos de preuba (Quitar cuando se lance el aplicativo) ---------------------
def insertarDatos(datos):
    mongo.db.coleccion_prueba.insert_one(datos)

#Función para mostrar la tabla creada
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

#Funición Query General 1
def obtenerDatosSqlServerXML(servidor, baseDatos, username, contrasena, consulta):
    # Connect to the database
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                'SERVER=' + servidor + ';'
                                'DATABASE=' + baseDatos + ';'
                                'UID=' + username + ';'
                                'PWD=' + contrasena)
    # Crear un objeto cursor
    cursor = conexion.cursor()

    # Ejecutar la consulta
    cursor.execute(consulta)

    # Obtener todos los resultados
    resultados = cursor.fetchall()

    # Convertir los resultados a una lista de diccionarios
    datos = [dict(zip([columna[0] for columna in cursor.description], fila)) for fila in resultados]

    # Convertir la lista de diccionarios a XML
    datos_xml = dicttoxml(datos)

    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()

    return datos_xml