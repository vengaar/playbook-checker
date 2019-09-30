import logging
import unittest
import copy
import re
from pathlib import Path
from pprint import pprint

import sys
sys.path.append('.')
import tests
from playbook_checker import PlaybookChecker


class TestPlaybookCheckSyntax(tests.TestPlaybookCheck):

    debug = False
    check_config = tests.get_check_config("config_syntax.yml")

    def test_ok(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/syntax/playbooks/ok*.yml')
        ]
#         pprint(reports)
        self.check_ok_reports(reports)

    def test_error(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in sorted(Path(tests._folder).glob('**/syntax/playbooks/error*.yml'))
        ]
        self.check_error_reports(reports)
#         pprint(reports)
        msg = reports[0]['errors'][0]['msg']
        self.assertTrue(msg.startswith("ERROR! The field 'hosts' has an invalid value"))
        msg = reports[1]['errors'][0]['msg']
        self.assertTrue(msg.startswith('while parsing a block collection'))
        msg = reports[2]['errors'][0]['msg']
        self.assertTrue(msg.startswith('ERROR! no action detected in task. This often indicates'))

    def test_warning(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/syntax/playbooks/warning*.yml')
        ]
        self.check_warning_reports(reports)
#         pprint(reports)
        msg = reports[0]['warnings'][0]['msg']
        expected_warning_pattern = ' [WARNING]: (Could not match supplied host pattern|provided hosts list is empty).*'
        expected_warning_pattern = r' \[WARNING\]: (Could not match supplied host pattern|provided hosts list is empty).*.*'
        self.assertIsNotNone(re.match(expected_warning_pattern, msg))

    def test_env(self):
        check_config = copy.deepcopy(self.check_config)
        check_config["syntax"] = {"env": {
                "ANSIBLE_FORCE_COLOR": "true",
            }
        }
        reports = [
            PlaybookChecker(path, check_config).info
            for path in Path(tests._folder).glob('**/syntax/playbooks/warning*.yml')
        ]
        msg = reports[0]['warnings'][0]['msg']
        self.assertTrue(msg.startswith('\x1b[1;35m [WARNING]'))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
