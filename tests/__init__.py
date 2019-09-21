import os
import sys

_current_file = os.path.abspath(__file__)
_folder = os.path.dirname(_current_file)
_folder_project = os.path.dirname(_folder)
_folder_lib = os.path.join(_folder_project, 'lib')

sys.path.append(_folder_lib)
