import json
import pika

with open("config_client.json", "r") as read_file:
    data = json.load(read_file)



conn = pika.BlockingConnection(pika.ConnectionParameters(
    data['host']))
chann = conn.channel(data['port'])

# declare a queue for recieved results
res = chann.queue_declare(exlusive=True)
count_queue = res.method.queue

def on_response(ch, method, props, body):
    
    ch.basic_publish(exchange='handler',
                     routing_key='request_queue',
                     body='Bring Me A Count!',
                     reply_to=count_queue,
                     delivery_mode=2)
    return 'The Request was sent'

conn.close()

