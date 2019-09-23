import logging
import unittest
from pathlib import Path
from pprint import pprint

import sys
sys.path.append('.')
import tests
from playbook_checker import PlaybookChecker


class TestPlaybookCheckDoc(tests.TestPlaybookCheck):

    check_config = tests.get_check_config("config_all.yml")

    def test_all(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob("**/playbooks/*.yml")
        ]
        #pprint(reports)
        for report in reports:
            if report["path"].endswith("syntax/playbooks/warning_hosts_undefined.yml"):
               self.assertEqual(len(report["warnings"]), 2) 


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
