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
        "check_syntax": True,
        "check_doc": False,
        "check_permissions": False,
    }

    def test_ok(self):
        report = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/syntax/playbooks/ok*.yml')
        ]
#         pprint(report)
        nb_report = len(report)
        self.assertEqual(nb_report, 1)
        for i in range(0, nb_report):
            self.assertEqual(report[0]["status"], "ok")
            self.assertEqual(report[0]["errors"], [])
            self.assertEqual(report[0]["warnings"], [])

    def test_ko(self):
        report = [
            PlaybookChecker(path, self.check_config).info
            for path in sorted(Path(tests._folder).glob('**/syntax/playbooks/error*.yml'))
        ]
#         pprint(report)
        nb_report = len(report)
        self.assertEqual(nb_report, 3)
        for i in range(0, nb_report):
            self.assertEqual(report[i]["status"], "error")
            self.assertEqual(len(report[0]["errors"]), 1)
            self.assertEqual(report[0]["warnings"], [])
        msg = report[0]["errors"][0]["msg"]
        self.assertTrue(msg.startswith("ERROR! The field 'hosts' has an invalid value"))
        msg = report[1]["errors"][0]["msg"]
        self.assertTrue(msg.startswith("while parsing a block collection"))
        msg = report[2]["errors"][0]["msg"]
        self.assertTrue(msg.startswith("ERROR! no action detected in task. This often indicates"))

    def test_warning(self):
        report = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/syntax/playbooks/warning*.yml')
        ]
#         pprint(report)
        nb_report = len(report)
        self.assertEqual(nb_report, 1)
        for i in range(0, nb_report):
            self.assertEqual(report[i]["status"], "warning")
            self.assertEqual(report[0]["errors"], [])
            self.assertEqual(len(report[0]["warnings"]), 1)
        msg = report[0]["warnings"][0]["msg"]
        self.assertTrue(msg.startswith(" [WARNING]: Could not match supplied host pattern"))

    def _test_all(self):
        report = [
            PlaybookChecker(path, self.check_config).info
            for path in Path(tests._folder).glob('**/syntax/playbooks/*.yml')
        ]
        pprint(report)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
