#!/usr/bin/env python3


"""
Module which uses consul to store and retrive
data from consul store
"""

import consul

from store.store import Store


class ConsulStore(Store):
    """
       Class which uses consul to store information
    """

    def __init__(self):
        """init method"""
        self._consul_conn = consul.Consul()

    def put(self, key, value):
        """
           Stores key and value in to Consul Store
        """
        try:
            self._consul_conn.kv.put(key, value)
        except Exception as err:
            print(f'Problem occured while writing key: {key}\
                  to consul: {err}')

    def get(self, key):
        """
           Retrieves the information from Consul Store
        """
        try:
            value = None
            data = self._consul_conn.kv.get(key)
            if data[1]:
                value = data[1]['Value'].decode()
            return value
        except Exception as err:
            print(f'Problem occured while reading key: {key}\
                  from consul: {err}')

    def delete(self, key):
        """
           Deletes information from the Consul Store
           specific to a user
        """
        try:
            self._consul_conn.kv.delete(key)
        except Exception as err:
            print(f'Problem occured while deleting the key: {key}\
                  from consul: {err}')

    def check_if_key_exists(self, key):
        '''check if key exist in the consul store'''
        if self.get(key):
            return True
        return False

    def update(self, key, value):
        """
           Updates the information in the Consul Store
           specific to a user
        """
        if self.check_if_key_exists(key):
            self.put(key, value)
            return
        print(f'key: {key} does not exist')
