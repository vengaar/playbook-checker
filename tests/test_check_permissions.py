import logging
import unittest
from pathlib import Path
from pprint import pprint

import sys
sys.path.append('.')
import tests
from playbook_checker import PlaybookChecker


class TestPlaybookCheckPermissions(tests.TestPlaybookCheck):

    debug = False
    check_config = tests.get_check_config("config_permissions.yml")

    def test_warning(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/permissions/playbooks/warning*.yml')
        ]
        pprint(reports)
        self.check_warning_reports(reports)
        msg = reports[0]['warnings'][0]['msg']
        self.assertEqual(msg, '0o644 instead 0o664')

    def _test_all(self):
        reports = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/permissions/playbooks/*.yml')
        ]
        self._debug(reports)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
