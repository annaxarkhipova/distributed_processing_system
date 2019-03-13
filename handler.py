import json
import pika


with open("config_handler.json", "r") as read_file:
    data = json.load(read_file)


conn = pika.BlockingConnection(pika.ConnectionParameters(
    data['host']))
chann = conn.channel(data['port'])







