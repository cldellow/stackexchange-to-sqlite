# stackexchange-to-sqlite

Export a Stack Exchange dump to a SQLite3 database.

# Usage

1. Pick a dump from https://tejp.de/files/so/dbdump/
    - One dump is included in the repo as cooking.stackexchange.2011-09-01.tar.zst
2. Unpack it into `input/`
3. `python3 convert.py`

Your database will be in `stack.db`
