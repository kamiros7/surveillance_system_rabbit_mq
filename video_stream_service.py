import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_initial_frame', exchange_type='topic')

routing_key = 'video.upload' #Maybe consider the input
message = 'frame_'.join(sys.argv[1]) or '0'
channel.basic_publish(
    exchange='topic_initial_frame', routing_key=routing_key, body=message)
print(f" [x] Sent {routing_key}:{message}")
connection.close()
