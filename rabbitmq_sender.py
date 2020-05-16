"""
Sender Module
"""


import json
from abc import ABCMeta, abstractmethod

import pika

msg = {"sender": "Madhura",
       "message": "I love Malhar A lottttt"
      }

class Sender(metaclass=ABCMeta):
    """Base class for all sender classes"""

    DEFAULT_HOST = 'localhost'

    def __init__(self, **kwargs):
        """Init Method"""
        self._host = kwargs.get('host')

    @abstractmethod
    def connect(self):
        '''Establishes a new connection'''
        raise NotImplementedError

    @abstractmethod
    def send(self, message):
        '''Sends a message'''
        raise NotImplementedError


class RabbitMQSender(Sender):
    """Sends message using RabbitMQ"""

    EXCHANGE_TYPE = 'fanout'
    ROUTING_KEY = ''
    CONTENT_TYPE = 'text/plain'

    def __init__(self, exchange_name, _host='localhost',
                 port=None):
        """Init Method"""
        super().__init__(host=_host)
        self._port = port
        self._exchange_name = exchange_name
        self._connection = None
        self._channel = None
        self._msg_props = pika.BasicProperties()
        self._msg_props.content_type = self.CONTENT_TYPE

    def connect(self):
        '''Establishes a new connection to RabbitMQ Server'''
        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(self._host))
            self._channel = self._connection.channel()
            self._channel.exchange_declare(exchange=self._exchange_name,
                                           exchange_type=self.EXCHANGE_TYPE,
                                           durable=True)
        except Exception as err:
            print(f'Error: {err}')

    def send(self, message):
        '''Sends a message to RabbitMQ Exchange'''
        try:
            self._channel.basic_publish(exchange=self._exchange_name,
                                        routing_key=self.ROUTING_KEY,
                                        properties=self._msg_props,
                                        body=message)
        except Exception as err:
            print(f'Error: {err}')


if __name__ == '__main__':
    sender = RabbitMQSender(exchange_name='tarpan', _host='localhost')
    sender.connect()
    sender.send(json.dumps(msg))

# TODO: Take message from User
# - Add RabbitMQ Port
# - Add Signal Catching Mechanism
# - Use of DEFAULT_HOST as a argument in __init__()
