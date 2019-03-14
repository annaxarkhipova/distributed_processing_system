import json
import pika
import time

with open("config_computer.json", "r") as read_file:
    data = json.load(read_file)



conn = pika.BlockingConnection(pika.ConnectionParameters(host=data['host'], port=data['port']))
chann = conn.channel()

channel.queue_declare(queue='task_queue', durable=True)
print('Waitin\' for new requests.')


def callback():
    print('Recieved a mail from handler.')
    sleeping = data['sleep']
    time.sleep(sleeping)
    print('Done')

   
    ch.basic_ack(delivery_tag = method.delivery_tag)


    # no more than 1 task for a computer
chann.basic_qos(prefetch_count=1)
    
# 'callback' in queue
chann.basic_consume(сallback,
                    queue='request_queue')


chann.start_consuming()
