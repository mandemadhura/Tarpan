#!/usr/bin/env python3


"""
Module which uses consul to store and retrive
data from consul store
"""


from store.store import Store

class ConsulStore(Store):
    """
       Class which uses consul to store information
    """

    def __init__(self):
        """init method"""
        super().__init__()

    def put(self, username, password):
        """
           Stores username and password in to Consul Store
        """
        pass

    def get(self, username):
        """
           Retrieves the information from Consul Store
        """
        pass

    def delete(self, username):
        """
           Deletes information from the Consul Store
           specific to a user
        """
        pass

    def update(self, username):
        """
           Updates the information in the Consul Store
           specific to a user
        """
        pass

