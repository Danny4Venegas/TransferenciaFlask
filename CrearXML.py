import xml.etree.ElementTree as ET

# Crea el elemento raíz del documento XML
root = ET.Element("persona")

# Crea los elementos hijo del elemento raíz
nombre = ET.SubElement(root, "nombre")
apellido = ET.SubElement(root, "apellido")
cedula = ET.SubElement(root, "cedula")

# Establece los valores de los elementos hijo
nombre.text = "Juan"
apellido.text = "Pérez"
cedula.text = "1234567890"

# Crea un objeto ElementTree a partir del elemento raíz
tree = ET.ElementTree(root)

# Guarda el documento XML en el archivo "persona.xml"
tree.write("persona.xml")