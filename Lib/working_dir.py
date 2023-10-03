import os
from pathlib import Path
from typing import Union
from contextlib import contextmanager


@contextmanager
def working_dir(path:Union[str, Path]):
    prev = os.getcwd()
    try:
        os.chdir(path)
        yield path
    except NotADirectoryError as err:
        print(err)
        print(f'Not a directory: {path}')
    finally:
        os.chdir(prev)
