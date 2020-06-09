#!/usr/bin/env python


'''
   Test module to check unit test functionality
   of sender module
'''


import unittest
from unittest.mock import patch

from sender import sender


class SenderTest(unittest.TestCase):
    '''
       Test class to check unit test functionality
       of sender module
    '''

    def setUp(self):
        '''Setup method for test suite'''
        print("inside setup")
        self.input_values = ['madhura', 'madhura123']
        self.output = []
        sender.input = self.mock_input
        sender.print = lambda std_print: self.output.append(std_print)

    def mock_input(self, stdin_inputs):
        '''Mocks the inbuilt input method of python3'''
        self.output.append(stdin_inputs)
        return self.input_values.pop(0)

    def test_input_stdin(self):
        '''
           test function to check functionality of input_stdin
           of sender module
        '''
        print('inside test_input_stdin')
        with patch('sender.sender.getpass.getpass') as mock_getpass:
            mock_getpass.return_value = self.input_values[1]
        sender.input_stdin()
        assert self.output == ['Enter User Name: ']

    def test_username_exists(self):
        '''
           test function to check functionality of username_exists
           of sender module
        '''
        with patch('sender.sender.requests.post') as mock_username_url:
            mock_username_url.return_value.status_code = 200
            username_exists = sender.username_exists(self.input_values[0])
            # mock_username_url.assert_called_with  ('http://localhost:6443/api/v1/user/check_user')
            self.assertEqual(username_exists, True)
