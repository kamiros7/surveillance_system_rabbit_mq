import pika

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_initial_frame', exchange_type='topic')
channel.exchange_declare(exchange='topic_processed_frame', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='topic_initial_frame', queue=queue_name, routing_key='video.#')

print(' [*] Waiting for images. To exit press CTRL+C')

routing_key = ''
def callback(ch, method, properties, body):
    print(f" [x] Received {body} with routing key {method.routing_key}")

    # Here i must be verify the message
    body += '_processed'
    ch.basic_publish(exchange='topic_processed_frame', routing_key=routing_key, body=body)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()

#validar as mensagens consumidas de video_stream
#imagem corrompida