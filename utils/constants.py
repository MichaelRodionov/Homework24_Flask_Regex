import os

# ----------------------------------------------------------------
# constants for application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")


COMMANDS = {'filter', 'map', 'unique', 'sort', 'limit', 'regex'}

SORT_PARAMS = {'asc', 'desc'}
