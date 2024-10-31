import pika, sys
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

def signMessage(message):
    #Assina a mensagem
    # Gerar o hash da mensagem
    hash_message = SHA256.new(message.encode())

    # Assinar o hash usando a chave privada
    signature = pkcs1_15.new(private_key).sign(hash_message)
    message += '|' + signature.hex()
    return message

# Carregar a chave privada do video_stream
with open("private_key.pem", "rb") as priv_file:
    private_key = RSA.import_key(priv_file.read())

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_initial_frame', exchange_type='topic')

routing_key = 'video.upload' #Maybe consider the input
#message = f'frame_{(sys.argv[1])}' + '|ASSINATURA' or 'frame_0' + 'teste'
message = f'frame_1' or 'frame_0' + 'teste'

message = signMessage(message)  #assina a mensagem

channel.basic_publish(
    exchange='topic_initial_frame', routing_key=routing_key, body=message)
print(f" [x] Sent {routing_key}:{message}")
connection.close()

