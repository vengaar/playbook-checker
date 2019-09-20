import logging
import unittest
from pathlib import Path

import os
_current_file = os.path.abspath(__file__)
_folder = os.path.dirname(_current_file)
_folder_project = os.path.dirname(_folder)
_folder_lib = os.path.join(_folder_project, 'lib', 'playbook-checker')
import sys
sys.path.append(_folder_lib)
from playbook_checker import *


class TestPlaybookCheck(unittest.TestCase):

    def test_all(self):
        check_config = {
            "check_permission": True,
            "permissions": {},
            "check_doc": True,
            "doc": {
                "type": "comment",
                "prefix": "#PLAYBOOK_DOC# ",
            },
            "check_syntax": True
        }
        playbook_inventory = [
            PlaybookCheck(path, check_config).info
            for path in Path(_folder).glob('**/playbooks/*.yml')
        ]
        print(Checkable.to_json(playbook_inventory))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
