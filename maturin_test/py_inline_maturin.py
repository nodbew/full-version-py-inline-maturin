import subprocess
import os
from pathlib import Path

from . import toml_util


def run(cmd: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell = True, check = True, **kwargs)
    

def initialize_maturin_project(path: str | Path = None, create: bool = False, name: str = None) -> None:
    
    '''Edit pyproject.toml and Cargo.toml to the maturin project style.'''

    # name and path defaults to each other
    if path is None:
        if name is None:
            raise ValueError("Either path or name has to be passed")
        else:
            path = f"./{name}"
    
    elif name is None:
        name = list(str(path).split("/"))[-1] # last directory in the path
    
    # create or look for the directory
    if create:
        run(f"maturin new -b pyo3 {path}")
    else:
        if not Path(str(path)).exists():
            raise FileNotFoundError(f"The directory('{Path(str(path)).resolve()}') does not exist")

    # Edit configuration
    toml_util.edit_pyproject_toml(path = f"{path}/pyproject.toml", name = name)
    toml_util.edit_cargo_toml(path = f"{path}/pyproject.toml", name = name)

    # look for src directory and lib.rs in it
    if Path(f'{path}/src').is_dir():
        if not Path(f'{path}/src/lib.rs').is_file():
            Path(f'{path}/src/lib.rs').touch()
    else:
        Path(f'{path}/src').mkdir()
        Path(f'{path}/src/lib.rs').touch()
        
    return

def build_maturin_project(path: str | Path) -> None:
    """
    Build a maturin project in the given name of directory.
    Uses maturin build -> pip install pattern.
    """
    
    # Search for the directory under the current directory
    if not Path(str(path)).is_dir():
        raise FileNotFoundError(f"There is no directory on {Path(str(path)).resolve()}")
    
    # build
    recent_working_dir = os.getcwd()
    os.chdir(str(path))
    run("maturin build --verbose")
    run("pip install ./target/wheels/*")
    os.chdir(recent_working_dir)

    return 
    

