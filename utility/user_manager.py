#!/usr/bin/env python3

"""
Module for User Registration for Authentication
"""

from utility.factory import get_store


class UserManager:
    """A class which implements functionality to create,
       store and retrieve user information
    """

    def __init__(self, store_name):
        """init method"""
        try:
            self._store_implementer = get_store(store_name)
        except KeyError as err:
            print(f'No module: {store_name} found to import')
        except Exception as err:
            print(f'Problem occured while getting the instance \
                  of the store: {err}')

    def create_user(self, user_name, user_password):
        """
           Creates and stores the information in the store
        """
        self._store_implementer.put(user_name, user_password)

    def check_existance_of_user(self, user_name):
        '''
            Checks whether User with username Exists in the store
            or not
        '''
        return self._store_implementer.check_if_key_exists(user_name)

    def get_password(self, user_name):
        """
           Authenticates the user with the information from store
        """
        password = None
        password = self._store_implementer.get(user_name)
        return password
