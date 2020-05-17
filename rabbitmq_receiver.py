"""
Receiver Module
"""

import json
import sys
from abc import ABCMeta, abstractmethod

import pika

QUEUE_NAME = "hello"

class Receiver(metaclass=ABCMeta):
    '''Abstract Base class for all receiver classes'''

    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = '5672'

    def __init__(self, _host, _port):
        '''Init Method'''
        self._host = _host or self.DEFAULT_HOST
        self._port = _port or self.DEFAULT_PORT

    @abstractmethod
    def connect(self):
        '''Establishes a new connection'''
        raise NotImplementedError

    @abstractmethod
    def receive(self):
        '''Receives a message'''
        raise NotImplementedError


class RabbitMQReceiver(Receiver):
    '''Receives a message using RabbitMQ'''

    EXCHANGE_TYPE = 'fanout'

    def __init__(self, **kwargs):
        '''Init Method'''

        super().__init__(kwargs.get('host'), kwargs.get('port'))
        self._exchange_name = kwargs.get('exchange_name')
        self._queue = kwargs.get('queue')
        self._routing_key = self._exchange_name
        self._auto_ack = True
        self._connection = None
        self._channel = None

    def connect(self):
        '''Establishes a new connection to RabbitMQ'''

        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self._host, port=self._port))
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self._queue)
            self._channel.exchange_declare(exchange=self._exchange_name,
                                           exchange_type=self.EXCHANGE_TYPE,
                                           durable=True)
            self._channel.queue_bind(queue=self._queue,
                                     exchange=self._exchange_name,
                                     routing_key=self._routing_key)
        except Exception as err:
            print(f'Error: {err}')

    def receive(self):
        '''Receives a message from RabbitMQ exchange and queue'''

        try:
            self._channel.basic_consume(
                queue=self._queue,
                on_message_callback=RabbitMQReceiver.callback,
                auto_ack=self._auto_ack)

            print(' [*] Waiting for messages. To exit press CTRL+C')
            self._channel.start_consuming()
        except Exception as err:
            print(f'Error: {err}')

    @staticmethod
    def callback(channel, method, properties, body):
        """Callback method for basic consume of RabbitMQ"""

        received_data = json.loads(body)
        print(f"{received_data['sender']}: {received_data['msg']}")

def usage():
    '''Prints the usage '''

    print('usage: rabbitmq_receiver.py queue_name \n \
          queue_name: Name of the queue')
    sys.exit(1)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Plese enter a valid argument')
        usage()

    # TODO: Get the username from the command line and
    # form a queue_name from it
    queue_name = sys.argv[1]

    receiver = RabbitMQReceiver(host='localhost', port=5672,
                                exchange_name='tarpan', queue=queue_name)
    receiver.connect()
    receiver.receive()
