import pika, sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_initial_frame', exchange_type='topic')

routing_key = 'video.upload' #Maybe consider the input
message = f'frame_{(sys.argv[1])}' or 'frame_0'
print(message)
channel.basic_publish(
    exchange='topic_initial_frame', routing_key=routing_key, body=message)
print(f" [x] Sent {routing_key}:{message}")
connection.close()
