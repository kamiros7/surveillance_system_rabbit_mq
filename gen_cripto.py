from Crypto.PublicKey import RSA

# Gerar um par de chaves RSA de 2048 bits
key = RSA.generate(2048)

# Exportar a chave privada e pública
private_key = key.export_key()
public_key = key.publickey().export_key()

# Salvar as chaves em arquivos PEM
with open("private_key2.pem", "wb") as priv_file:
    priv_file.write(private_key)

with open("public_key2.pem", "wb") as pub_file:
    pub_file.write(public_key)

print("Chaves RSA geradas e salvas.")