"""
    @author: Olivier Perriot
"""

import os
import stat
import json
import yaml
import logging
import subprocess
from pathlib import Path
from typing import Dict

# project import
from .utils import to_json

DEFAULT_PLAYBOOKS_CHECKS_CONFIG = {
    "check_syntax": True,
    "check_doc": False,
    "check_permissions": False,
    "doc": {
        "type": "comment",
        "prefix": "#PLAYBOOK_DOC# ",
        "authors": ["vengaar", "foo", "bar"]
    },
    "permissions": {
        "owner": "foo",
        "group": "foo",
        "mode": "0o664",
    }
}


class Checkable(object):

    OK = "ok"
    INFO = "info"
    ERROR = "error"
    WARNING = "warning"
    CRITICITIES = (INFO, WARNING, ERROR)

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.infos = []
        self.errors = []
        self.warnings = []

    def _add_issue(self, criticity, type, msg):
        assert(criticity in self.CRITICITIES)
        issue = {"type": type, "msg": msg}
        if criticity == self.ERROR:
            self.errors.append(issue)
        elif criticity == self.WARNING:
            self.warnings.append(issue)

    @staticmethod
    def to_json(data):
        return json.dumps(data, indent=2, sort_keys=True)

    @property
    def info(self):
        info = {
            key: self.__dict__[key]
            for key in self.__dict__
            if not key.startswith('_')
        }
        info["status"] = self.status
        return info

    @property
    def status(self):
        status = "ok"
        if len(self.warnings) > 0:
            status = self.WARNING
        if len(self.errors) > 0:
            status = self.ERROR
        return status

    def __str__(self, *args, **kwargs):
        return to_json(self.info)


class PlaybookChecker(Checkable):

    def __init__(self, path: Path, check_config: Dict={}):
        super().__init__()
        self._config = DEFAULT_PLAYBOOKS_CHECKS_CONFIG if check_config == {} else check_config
        self._logger.debug(self._config)
        self._logger.info(path)
        self._path = path
        self.path = str(path)
        project_playbooks = os.path.dirname(self.path)
        self.project_path = os.path.dirname(project_playbooks)
        self.project = os.path.basename(self.project_path)
        try:
            with open(self.path) as fp:
                self._playbook = yaml.safe_load(fp)
        except (yaml.scanner.ScannerError,
            yaml.parser.ParserError) as err:
            self._add_issue(self.ERROR, "playbook > yaml parsing", str(err))
        except Exception as err:
            self._add_issue(self.ERROR, "playbook > yaml parsing", str(err))
        else:
            self._logger.debug(self._playbook)
            if self._config["check_syntax"]:
                self._check_syntax()
            if self._config["check_doc"]:
                self._check_doc()
            if self._config["check_permissions"]:
                self._check_permissions()

    def _check_syntax(self):
            command = [
                "ansible-playbook",
                "--syntax-check",
                self.path,
            ]
            process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.syntax = (process.stderr == b"")
            if not self.syntax:
                self._logger.debug(process.stderr)
                stderr = str(process.stderr, "utf-8")
                if process.returncode == 0:
                    self._add_issue(self.WARNING, "playbook > syntax-check", stderr)
                else:
                    self._add_issue(self.ERROR, "playbook > syntax-check", stderr)

    def _check_permissions(self):
        permissions = self._config["permissions"]
        if "mode" in permissions:
            mode = oct(stat.S_IMODE(self._path.stat().st_mode))
            self._logger.debug(mode)
            mode_expected = permissions["mode"]
            if mode != mode_expected:
                msg = "{found} instead {expected}".format(found=mode, expected=mode_expected)
                self._add_issue(self.WARNING, "permission > mode", msg)

        if "owner" in permissions:
            owner = self._path.owner()
            self._logger.debug(owner)
            owner_expected = permissions["owner"]
            if owner != owner_expected:
                msg = "{found} instead {expected}".format(found=owner, expected=owner_expected)
                self._add_issue(self.ERROR, "permission > owner", msg)

        if "group" in permissions:
            group = self._path.group()
            self._logger.debug(group)
            group_expected = permissions["group"]
            if group != group_expected:
                msg = "{found} instead {expected}".format(found=group, expected=group_expected)
                self._add_issue(self.ERROR, "permission > group", msg)

    def _check_doc(self):
        doc = self._extract_doc()
        if doc is not None:
            self.description = doc.get("description")
            if not "author" in doc:
                self._add_issue(self.ERROR, "doc", "Missing author")
            else:
                self.author = doc["author"]
                if self.author not in self._config["doc"]["authors"]:
                    self._add_issue(self.ERROR, "doc", "Invalid author")

    def _extract_doc(self):
        prefix = self._config["doc"]["prefix"]
        with open(self.path) as fp:
            lines = [
                line[len(prefix):]
                for line in fp
                if line.startswith(prefix)
            ]
            if len(lines) > 0:
                raw_doc = "".join(lines)
                try:
                    doc = yaml.safe_load(raw_doc)
                    self._logger.debug(doc)
                    return doc
                except (yaml.scanner.ScannerError,
                    yaml.parser.ParserError) as err:
                    self._add_issue(self.ERROR, "doc > yaml parsing", str(err))
                except Exception as err:
                    self._add_issue(self.ERROR, "doc > yaml parsing", str(err))
            else:
                self._add_issue(self.WARNING, "doc", "Doc missing")
