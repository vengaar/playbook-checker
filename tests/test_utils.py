import logging
import unittest
from pprint import pprint
import os

import sys
sys.path.append(".")
import tests
from playbook_checker import read_config, to_json

class TestPlaybookCheck(unittest.TestCase):

    config_file = os.path.join(tests._folder, "data", "config_all.yml")

    def test_read_config(self):
        check_config = read_config(self.config_file)
        self.assertTrue(check_config["check_syntax"])
        self.assertTrue(check_config["check_doc"])
        self.assertTrue(check_config["check_permissions"])
        self.assertEqual(check_config["permissions"]["mode"], "0o664")
        self.assertEqual(check_config["doc"]["prefix"], "#PLAYBOOK_DOC# ")

    def test_to_json(self):
        check_config = read_config(self.config_file)
        str_json = to_json(check_config)
#         print(str_json)
        expected = """{
  "check_doc": true,
  "check_permissions": true,
  "check_syntax": true,
  "doc": {
    "fields": [
      {
        "expected": [
          "foo",
          "bar"
        ],
        "name": "author",
        "required": true
      },
      {
        "name": "description",
        "required": true
      }
    ],
    "prefix": "#PLAYBOOK_DOC# ",
    "required": false,
    "type": "comment"
  },
  "permissions": {
    "group": "vengaar",
    "mode": "0o664",
    "owner": "vengaar"
  }
}"""
        self.assertEqual(str_json, expected)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
