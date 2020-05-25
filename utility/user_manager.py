#!/usr/bin/env python3

"""
Module for User Registration for Authentication
"""

from store.store import Store
from utility.factory import get_store

class UserManager:
    """A class which implements functionality to create,
       store and retrieve user information
    """

    def __init__(self, store_name):
        """init method"""
        self._store_implementer = get_store(store_name)

    def create_user(self, user_name, user_password):
        """
           Creates and stores the information in the store
        """
        pass

    def authenticate_user(self, user_name, user_password):
        """
           Authenticates the user with the information from store
        """
        pass
