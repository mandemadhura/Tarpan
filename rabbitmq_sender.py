"""
Sender Module
"""


import json
import sys

import pika


message = {"sender": "Madhura",
           "message": "I love Malhar A lottttt"
          }

if len(sys.argv) == 2:
    message = sys.argv[1]

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='tarpan', exchange_type='fanout', durable=True)
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
channel.basic_publish(exchange='tarpan', routing_key='',
                      properties=msg_props, body=json.dumps(message))


print(" [x] Sent 'Hello World!'")
