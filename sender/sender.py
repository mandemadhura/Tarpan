#!/usr/bin/env python

"""
Sender Module
"""


import getpass
import json
import sys
from abc import ABCMeta, abstractmethod

import pika
import requests


class Sender(metaclass=ABCMeta):
    '''Base class for all sender classes'''

    DEFAULT_HOST = 'localhost'

    def __init__(self, **kwargs):
        '''Init Method'''
        self._host = kwargs.get('host')

    @abstractmethod
    def connect(self):
        '''Establishes a new connection'''
        raise NotImplementedError

    @abstractmethod
    def send(self, msg):
        '''Sends a message'''
        raise NotImplementedError


class RabbitMQSender(Sender):
    '''Sends message using RabbitMQ'''

    EXCHANGE_TYPE = 'fanout'
    ROUTING_KEY = ''
    CONTENT_TYPE = 'text/plain'

    def __init__(self, exchange_name, _host='localhost',
                 port=None):
        '''Init Method'''
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
                pika.ConnectionParameters(self._host, self._port))
            self._channel = self._connection.channel()
            self._channel.exchange_declare(exchange=self._exchange_name,
                                           exchange_type=self.EXCHANGE_TYPE,
                                           durable=True)
        except Exception as err:
            print(f'Error: {err}')
            sys.exit(1)

    def send(self, msg):
        '''Sends a message to RabbitMQ Exchange'''
        try:
            self._channel.basic_publish(exchange=self._exchange_name,
                                        routing_key=self.ROUTING_KEY,
                                        properties=self._msg_props,
                                        body=msg)
        except Exception as err:
            print(f'Error: {err}')
            sys.exit(1)


def authenticate(username, pwd):
    '''Authenticates User'''
    url = 'http://localhost:6443/api/v1/user'
    response = requests.post(f'{url}/{username}/authenticate',
                             json={"password": f"{pwd}"})
    return response.status_code == 200

def add_user(username, pwd):
    '''Registers user's information to the store'''
    url = 'http://localhost:6443/api/v1/user/users'
    response = requests.post(f'{url}/{username}/add_user',
                             json={"password": f"{pwd}"})
    return response.status_code == 201

def username_exists(username):
    '''Checks whether user is already registred or not'''
    url = 'http://localhost:6443/api/v1/user'
    response = requests.post(f'{url}/check_user',
                             json={"username": f"{username}"})
    return response.status_code == 200

def input_stdin():
    '''Accepts the input from stdin'''
    username = input('Enter User Name: ').strip()
    if len(username) == 0:
        print("User Name can not be blank")
        sys.exit(1)
    password = getpass.getpass()
    return username, password


if __name__ == '__main__':
    EXIT_CMD = 'q!'
    CONTINUE = 'c'
    RETRY_COUNT = 0

    user_name, passwd = input_stdin()
    if not username_exists(user_name):
        INPUT_CMD = input('Please register first to use the messenger.\n\
                          Press c to continue with registration.\n\
                          press q! to quit. \n')
        if INPUT_CMD == CONTINUE:
            user_name, passwd = input_stdin()
            if not add_user(user_name, passwd):
                print('Problem occured while registration. Please try again')
                sys.exit(1)
            INPUT_CMD = input('Press c to continue with login. press q! to quit. \n')
            if INPUT_CMD == EXIT_CMD:
                sys.exit(0)
            user_name, passwd = input_stdin()
        else:
            sys.exit(1)

    authenticated = authenticate(user_name, passwd)
    if not authenticated:
        print('Invalid Username or password')
        sys.exit(1)

    sender = RabbitMQSender(exchange_name='tarpan', _host='localhost',
                            port='5672')
    sender.connect()

    INPUT_MSG = ''
    message = {}
    while True:
        INPUT_MSG = input('Enter message to send. Press q! to quit. \n')
        if INPUT_MSG == EXIT_CMD:
            break
        if len(INPUT_MSG.strip()) > 0:
            message['sender'] = user_name
            message['msg'] = INPUT_MSG
            print(message)
            sender.send(json.dumps(message))
    print("Exiting...")

# - Add Signal Catching Mechanism
# - Use of DEFAULT_HOST as a argument in __init__()
# - If Connection Fails, retry machanism to connect to RabbitMQ
