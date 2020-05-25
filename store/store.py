#!/usr/bin/env python3


"""
Module for all the store implementation
"""


class Store:
    """
       Base interface which provides functionality to add,
       retrieve, update and delete the information from the
       store
    """

    def __init__(self):
        """init method"""
        pass

    def put(self, username, password):
        """
           Add the new information in the store
        """
        raise NotImplementedError

    def get(self, username):
        """
           Retrieves the information specific to
           username from the store
        """
        raise NotImplementedError

    def delete(self, username):
        """
           Deletes the information specific to
           username from the store
        """
        raise NotImplementedError

    def update(self, username):
        """
           Updates the information specific to
           username in the store
        """
        raise NotImplementedError

