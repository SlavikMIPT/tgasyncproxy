#!/usr/bin/python3.7
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest


class TestBasicMethods(unittest.TestCase):
    def test_api_token_provided(self):
        self.assertIsNotNone(os.environ.get('BOT_TOKEN'))

    def test_api_url_provided(self):
        self.assertIsNotNone(os.environ.get('API_URL'))


if __name__ == '__main__':
    unittest.main()
