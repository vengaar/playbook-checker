import logging
import unittest
from pathlib import Path
import os
from pprint import pprint

import sys
sys.path.append(".")
import tests
from playbook_checker import PlaybookChecker


class TestPlaybookCheck(unittest.TestCase):

    check_config = {
        "check_syntax": False,
        "check_doc": False,
        "check_permissions": True,
        "permissions": {
            "owner": "vengaar",
            "group": "vengaar",
            "mode": "0o664",
        }
    }

    def test_all(self):
        report = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/permissions/playbooks/*.yml')
        ]
        pprint(report)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
