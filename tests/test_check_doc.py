import logging
import unittest
from pathlib import Path

import sys
sys.path.append('.')
import tests
from playbook_checker import PlaybookChecker


class TestPlaybookCheckDoc(tests.TestPlaybookCheck):

    debug = False
    check_config = tests.get_check_config("config_doc.yml") 

    def test_ok(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/doc/playbooks/ok*.yml')
        ]
        self.check_ok_reports(reports)

    def test_error(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/doc/playbooks/error*.yml')
        ]
        self.check_error_reports(reports)

    def test_warning(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/doc/playbooks/warning*.yml')
        ]
        self.check_warning_reports(reports)
        self.assertEqual(reports[0]['warnings'][0]['msg'], 'Doc missing')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
