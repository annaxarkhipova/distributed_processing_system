import json
import pika
import time

with open("config_computer.json", "r") as read_file:
    data = json.load(read_file)


conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) #data['host'], port=data['port'])
channel = conn.channel()

channel.queue_declare(queue='task_queue')




def callback_to_request(ch, method, properties, body):
    print('Received %r' % body)
    print('Start PDF processing')
    sleeping = data['sleep']
    time.sleep(sleeping)


    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                     properties.correlation_id),
                     body='Finished')

    # Если подписчик прекратил работу и не отправил подтверждение,
    # RabbitMQ поймет, что сообщение не было обработано, и передаст его другому подписчику
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1) # no more than 1 queue for a consumer
channel.basic_consume(callback_to_request, queue='task_queue')

print('Awaiting RPC requests')
channel.start_consuming()




