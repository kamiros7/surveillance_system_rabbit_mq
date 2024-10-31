import pika
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# Carregar a chave pública do video_stream
with open("public_key.pem", "rb") as pub_file:
    public_key = RSA.import_key(pub_file.read())

# Carregar a chave privada do preprocessor
with open("private_key2.pem", "rb") as priv_file:
    private_key = RSA.import_key(priv_file.read())

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_initial_frame', exchange_type='topic')
channel.exchange_declare(exchange='topic_processed_frame', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='topic_initial_frame', queue=queue_name, routing_key='video.#')

print(' [*] Waiting for images. To exit press CTRL+C')

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

def signMessage(message):
    #Assina a mensagem
    # Gerar o hash da mensagem
    hash_message = SHA256.new(message.encode())

    # Assinar o hash usando a chave privada
    signature = pkcs1_15.new(private_key).sign(hash_message)
    message += '|' + signature.hex()
    return message

routing_key = ''
def callback(ch, method, properties, body):
    isValidSignature = checkSignature(body)
    if (isValidSignature):
        print("Message accepted: valid signature.") 
        print(f" [x] Received {body} with routing key {method.routing_key}")
        message = body.decode('utf-8')
        # Here i must be verify the message
        message = message.split('|')[0] #ignorando o conteudo de assinatura
        message += '_processed'
        message = signMessage(message)
        new_body = message.encode('utf-8')
        ch.basic_publish(exchange='topic_processed_frame', routing_key=routing_key, body=new_body)
    else:
        print("Message not accepted: invalid signature.") 

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()

#validar as mensagens consumidas de video_stream
#imagem corrompida