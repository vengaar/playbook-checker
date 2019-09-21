import os
import sys

_current_file = os.path.abspath(__file__)
_folder = os.path.dirname(_current_file)
_folder_project = os.path.dirname(_folder)
_folder_lib = os.path.join(_folder_project, 'lib')

_config_file = os.path.join(_folder, "data", "config.yml")

sys.path.insert(0, _folder_lib)
