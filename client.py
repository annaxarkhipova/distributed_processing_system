import json
import pika

with open("config_client.json", "r") as read_file:
    data = json.load(read_file)


class System:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
                #host=data['host'], port=data['port']))
        self.channel = self.connection.channel()

        # durable - очередь не будет потеряна при падении сервера
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


    def call(self):
        self.response = None
        self.channel.basic_publish(exchange='',
                                   routing_key='task_queue',
                                   delivery_mode = 2, # сообщения не будут утеряны
                                   properties=pika.BasicProperties(
                                         reply_to=self.callback_queue,
                                         correlation_id=self.corr_id,
                                   body='Please, make a count for me and bring it back!'))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


response = System()

print('Sending a please to process PDF file')
calling = response.call()
print('Got a reply %r' % (response,))