"""
    @author: Olivier Perriot
"""

# std import
import argparse
import logging
import os
import json
from pathlib import Path

# project import
from .checker import PlaybookChecker
from .utils import to_json, read_config

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
        '--config',
        action='store',
        type=str,
        help='The path of a checks configation file'
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
    logger = logging.getLogger(__name__)
    logger.info(args)
    
    if args.config is not None:
        config = read_config(args.config)
        logger.debug(config)
    else:
        config = {}
    absolute_path = os.path.expanduser(args.path)
    report = [
        PlaybookChecker(path, config).info
        for path in Path(absolute_path).glob("**/playbooks/*.yml")
    ]
    if args.dump:
        print(to_json(report))
    else:
        report_file = args.out
        with open(report_file, "w") as fp:
            json.dump(report, fp, indent=2, sort_keys=True)
        result = {
            "report": report_file,
            "To read it": "jq . {file}".format(file=report_file)
        }
        print(to_json(result))

if __name__ == '__main__':
    main()
