import pika

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
    print(f" [x] Received {body} with routing key {method.routing_key}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()

#validar as mensagens consumidas de preprocessor
#imagem corrompida