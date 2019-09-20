"""
    @author: Olivier Perriot
"""

import argparse
import logging
import os
from pathlib import Path
from playbook_checker import *


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--path',
        action='store',
        default='~',
        type=str,
        help='The path where search playbooks, example ~/myproject'
    )
    parser.add_argument(
        '--pattern',
        action='store',
        default='**/playbooks/*.yml',
        type=str,
        help='The pattern to used to search playbooks in path. Example **/playbooks/*.yml'
    )
    parser.add_argument(
        '--log-level',
        action='store',
        choices=logging._nameToLevel,
        default='INFO',
        type=str,
        help='The log level to used'
    )
    parser.add_argument(
        '--dump',
        action='store_true',
        help='To display report on output'
    )
    parser.add_argument(
        '--out',
        action='store',
        default='/tmp/playbooks_checks.report.json',
        type=str,
        help='The path where write the report'
    )
    args = parser.parse_args()
    logging_level = logging.getLevelName(args.log_level)
    logging.basicConfig(level=logging_level)
    absolute_path = os.path.expanduser(args.path)
    report = [
        PlaybookCheck(path).info
        for path in Path(absolute_path).glob(args.pattern)
    ]
    if args.dump:
        print(Checkable.to_json(report))
    else:
        with open(args.out, "w") as fp:
            json.dump(report, fp, indent=2, sort_keys=True)


if __name__ == '__main__':
    main()
