import pika
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# Carregar a chave pública do preprocessor
with open("public_key2.pem", "rb") as pub_file:
    public_key = RSA.import_key(pub_file.read())

def checkSignature(body):
    message = body.decode('utf-8').split('|')[0]
    hash_message = SHA256.new(message.encode())
    signature_hex = body.decode('utf-8').split('|')[1]
    signature = bytes.fromhex(signature_hex)
    try:
        # Verificar a assinatura usando a chave pública
        pkcs1_15.new(public_key).verify(hash_message, signature)
        print("Assinatura válida: A mensagem é autêntica.")
        return True
    except (ValueError, TypeError):
        return False

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_processed_frame', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='topic_processed_frame', queue=queue_name, routing_key='')

print(' [*] Waiting for processed images. To exit press CTRL+C')

routing_key = ''
def callback(ch, method, properties, body):
    isValidSignature = checkSignature(body)
    if (isValidSignature):
        print("Message accepted: valid signature.") 
        print(f" [x] Received {body} with routing key {method.routing_key}")
    else:
        print("Message not accepted: invalid signature.") 

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()

#validar as mensagens consumidas de preprocessor
#imagem corrompida