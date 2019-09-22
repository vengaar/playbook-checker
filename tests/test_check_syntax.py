import logging
import unittest
from pathlib import Path
import os
from pprint import pprint

import sys
sys.path.append('.')
import tests
from playbook_checker import PlaybookChecker


class TestPlaybookCheckSyntax(tests.TestPlaybookCheck):

    debug = False
    check_config = {
        'check_syntax': True,
        'check_doc': False,
        'check_permissions': False,
    }

    def test_ok(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/syntax/playbooks/ok*.yml')
        ]
        self.check_ok_reports(reports)

    def test_error(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in sorted(Path(tests._folder).glob('**/syntax/playbooks/error*.yml'))
        ]
        self.check_error_reports(reports)
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
        msg = reports[0]['warnings'][0]['msg']
        self.assertTrue(msg.startswith(' [WARNING]: Could not match supplied host pattern'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
