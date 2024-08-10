import subprocess
import os
from pathlib import Path

import toml


class InvalidConfigError(Exception):pass
    

def run(cmd: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell = True, check = True, **kwargs)
    

def initialize_maturin_project(path: str, create: bool = False, name: str = None) -> None:
    
    '''Edit pyproject.toml and Cargo.toml to the maturin project style.'''

    # Name defaults to the directory name
    if name is None:
        name = list(str(path).split("/"))[-1] # last directory in the path
    
    if create:
        run(f"maturin new -b pyo3 ./{path}")
    else:
        if not Path(f"./{path}").exists():
            raise FileNotFoundError(f"The directory('{Path(f'./{path}').resolve()}') does not exist")

    _edit_pyproject_toml(path = f"./{path}/pyproject.toml", name = name)
    _edit_cargo_toml(path = f"./{path}/pyproject.toml", name = name)

    # look for src directory and lib.rs in it
    if Path(f'./{name}/src').is_dir():
        if not Path(f'./{name}/src/lib.rs').is_file():
            Path(f'./{name}/src/lib.rs').touch()
    else:
        Path(f'./{name}/src').mkdir()
        Path(f'./{name}/src/lib.rs').touch()
        
    return

def build_maturin_project(name: str) -> None:
    """
    Build a maturin project in the given name of directory.
    Uses maturin build -> pip install pattern.
    """
    if not isinstance(name, str):
        raise TypeError(f'The "name" argument must be a str, not {type(name)}')

    # Search for the directory under the current directory
    if not Path('./' + str(name)).is_dir():
        raise FileNotFoundError(f"There is no directory named {name}")
    
    # build
    recent_working_dir = os.getcwd()
    os.chdir('./' + str(name))
    run("maturin build --verbose")
    run("pip install ./target/wheels/*")
    os.chdir(recent_working_dir)

    return 
    

