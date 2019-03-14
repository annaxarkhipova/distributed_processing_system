import json
import pika


with open("config_computer.json", "r") as read_file:
    data = json.load(read_file)

conn = pika.BlockingConnection(pika.ConnectionParameters(host=data['host'], port=data['port']))
chann = conn.channel()

channel.queue_declare(queue='task_queue', durable=True)
print('Waitin\' for new requests.')



def on_request(ch, method, props, body):
    response = 'OK, sending to a computer ..'
    print(response)

    ch.basic_publish(exchange='',
                     routing_key='task_queue')

    ch.basic_ack(delivery_tag = method.delivery_tag)


    # telling that 'callback' should recieve message from queue
chann.basic_consume(on_request,
                    queue='request_queue')


chann.start_consuming()










