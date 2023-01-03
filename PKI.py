from OpenSSL import crypto

# Genera una clave privada
key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

# Serializa la clave privada a PEM
private_key_pem = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)

# Guarda la clave privada a un archivo
with open('private_key.pem', 'wb') as key_file:
    key_file.write(private_key_pem)

# Serializa la clave pública a PEM
public_key_pem = crypto.dump_publickey(crypto.FILETYPE_PEM, key)

# Guarda la clave pública a un archivo
with open('public_key.pem', 'wb') as key_file:
    key_file.write(public_key_pem)

# Genera una solicitud de firma de certificado (CSR)
csr = crypto.X509Req()
csr.set_pubkey(key)
csr.sign(key, 'sha256')

# Serializa el CSR a PEM
csr_pem = crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr)

# Guarda el CSR a un archivo
with open('csr.pem', 'wb') as csr_file:
    csr_file.write(csr_pem)

# Firma el CSR y genera un certificado autofirmado
certificate = crypto.X509()
certificate.set_subject(csr.get_subject())
certificate.set_pubkey(csr.get_pubkey())
certificate.sign(key, 'sha256')

# Serializa el certificado a PEM
certificate_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, certificate)

# Guarda el certificado a un archivo
with open('certificate.pem', 'wb') as certificate_file:
    certificate_file.write(certificate_pem)

