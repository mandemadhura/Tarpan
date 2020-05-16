"""
Receiver Module
"""

import json
import sys

import pika


QUEUE_NAME = "hello"

def callback(channel, method, properties, body):
    """Callback method for basic consume of RabbitMQ"""

    received_data = json.loads(body)
    print(f"{received_data['sender']}: {received_data['msg']}")


if len(sys.argv) == 2:
    QUEUE_NAME = sys.argv[1]

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)
channel.exchange_declare(exchange='tarpan', exchange_type='fanout', durable=True)
channel.queue_bind(queue=QUEUE_NAME, exchange='tarpan', routing_key='tarpan')
channel.basic_consume(on_message_callback=callback, queue=QUEUE_NAME)


channel.basic_consume(
    queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
