import json
import pika
import time

with open("config_computer.json", "r") as read_file:
    data = json.load(read_file)

conn = pika.BlockingConnection(pika.ConnectionParameters(data['host']))
chann = conn.channel(data['port'])

# if connection is closed, the queue should be deleted, so flag's:
chann.queue_declare(queue='request_queue')
print('Waitin\' for new requests.')



# binding the hadler and computer (tell the handler to send messages to our queue)
#chann.queue_bind(exchange='logs')


def callback():
    print('Recieved a mail from client. Counting ..')
    sleeping = data['sleep']
    time.sleep(sleeping)
    print('Done')

def reply_on(ch, method, props, body):
    print(body) # ???

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     body='Replied to client')
    ch.basic_ack(delivery_tag = method.delivery_tag) # ???


    # no more than 1 task for a computer
chann.basic_qos(prefetch_count=1)
    
    # telling that 'callback' should recieve message from queue
chann.basic_consume(callback,
                    queue='request_queue')
chann.start_consuming()

