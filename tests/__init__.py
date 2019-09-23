import os
import sys
import unittest
from pprint import pprint

_current_file = os.path.abspath(__file__)
_folder = os.path.dirname(_current_file)
_folder_project = os.path.dirname(_folder)
_folder_lib = os.path.join(_folder_project, 'lib')
sys.path.insert(0, _folder_lib)

from playbook_checker import read_config

def get_check_config(name):
    config_file = os.path.join(_folder, "data", name)
    return read_config(config_file)

class TestPlaybookCheck(unittest.TestCase):

    debug = True

    def _debug(self, data):
        if self.debug:
            pprint(data)

    def check_ok_reports(self, reports):
        self._debug(reports)
        for i in range(0, len(reports)):
            self.assertEqual(reports[i]["status"], "ok")
            self.assertEqual(reports[0]["errors"], [])
            self.assertEqual(reports[0]["warnings"], [])

    def check_error_reports(self, reports):
        self._debug(reports)
        for i in range(0, len(reports)):
            self.assertEqual(reports[0]["status"], "error")
            self.assertEqual(len(reports[0]["errors"]), 1)
            self.assertEqual(reports[0]["warnings"], [])

    def check_warning_reports(self, reports):
        self._debug(reports)
        for i in range(0, len(reports)):
            self.assertEqual(reports[i]["status"], "warning")
            self.assertEqual(reports[0]["errors"], [])
            self.assertEqual(len(reports[0]["warnings"]), 1)
