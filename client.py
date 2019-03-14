import json
import pika

with open("config_client.json", "r") as read_file:
    data = json.load(read_file)



class System:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=data['host'], port=data['port'])) # data['port'] ???

        self.channel = self.connection.channel()

        # объявляем  очередь результатов для полученных ответов
        result = self.channel.queue_declare(queue='task_queue', durable=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
        # basic_consume это ???


        # Функция обратного вызова 'on_response', 
        # исполнямая при получении каждого ответа, 
        # выполняет довольно тривиальную задачу — 
        # для каждого поступившего ответа она проверяет 
        # соответствует ли correlation_id тому что мы ожидаем. 
        # Если это так, она сохраняет ответ в self.response и 
        # прерывает цикл

    def on_response(self, ch, method, props, body):
        if self.corr_id is True:
            self.response = body

    def call(self, n):
        self.response = None
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                   body='I\'m done with computing'))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    print('Please, make a count')
    response = System()
    calling = responce.call()
    print('Got', calling)
