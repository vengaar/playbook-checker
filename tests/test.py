import logging
import unittest
from pathlib import Path
import os

import sys
sys.path.append(".")
import tests

import playbook_checker
from playbook_checker import PlaybookChecker
from playbook_checker import read_config, to_json

class TestPlaybookCheck(unittest.TestCase):

    def test_ok(self):
        config_file = os.path.join(tests._folder, "data", "config.yml")
        check_config = read_config(config_file)
        path = Path(os.path.join(tests._folder, "data", "ok", "playbooks", "ok.yml"))
        pc = PlaybookChecker(path, check_config)
        print(pc)

    def test_all(self):
        config_file = os.path.join(tests._folder, "data", "config.yml")
        check_config = read_config(config_file)
        playbook_inventory = [
            PlaybookChecker(path, check_config).info
            for path in Path(tests._folder).glob('**/playbooks/*.yml')
        ]
        print(to_json(playbook_inventory))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#     logging.basicConfig(level=logging.ERROR)
    unittest.main()
