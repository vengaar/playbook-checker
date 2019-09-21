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
        "check_doc": True,
        "check_permissions": False,
        "doc": {
            "type": "comment",
            "prefix": "#PLAYBOOK_DOC# ",
            "authors": ["vengaar", "foo", "bar"]
        },
    }

    def test_all(self):
        report = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/doc/playbooks/*.yml')
        ]
        pprint(report)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
