import subprocess
import os
from pathlib import Path
from typing import Literal

import toml_util


def run(cmd: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell = True, check = True, **kwargs)
    

def initialize_maturin_project(
        path: str | Path = None, 
        create: bool = False, 
        name: str = None,
        mode: Literal["r", "rp"] = "r",
    ) -> None:
    
    '''
    
    Edit pyproject.toml and Cargo.toml to the maturin project style.
    
    Parameters:
        path: A path to the project directory. If omitted, defaults to "./{name}".
        create: Whether to create a new project directory or not.
        name: A name of the project. If omitted, defaults to the deepest directory's name in the path argument.
        mode: A layout of the project. 
              "r" stands for a pure-Rust project, and "rp" stands for a Rust-Python combined project.
            
    Errors: 
        ValueError: When both path and name arguments are omitted.
        CalledProcessError: A general exception that is raised when maturin fails to create a new project on the given directory.
                            A common cause is that the directory already exists.
        FileNotFoundError: When there is no directory in the path, and create argument is set to false.
        InvalidConfigError: Raised when a required setting, such as "project" section in pyproject.toml, is missing.
        TomlDecodeError: A general exception raised when the toml library fails to analyze either pyproject.toml or Cargo.toml.
        
    '''

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
        try:
            run(f"maturin new -b pyo3 --name {name} {path}")
        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(f"Maturin failed to create a new project on the given directory. \nPerhaps it already exists? \nCaptured stdere call: \n{e.output}")
    else:
        if not Path(str(path)).is_dir():
            raise FileNotFoundError(f"The directory('{Path(str(path)).resolve()}') does not exist")

    # Edit configuration
    toml_util.edit_pyproject_toml(path = f"{path}/pyproject.toml", name = name)
    toml_util.edit_cargo_toml(path = f"{path}/Cargo.toml", name = name)

    # look for src directory and lib.rs in it
    if Path(f'{path}/src').is_dir():
        if not Path(f'{path}/src/lib.rs').is_file():
            Path(f'{path}/src/lib.rs').touch()
    else:
        Path(f'{path}/src').mkdir()
        Path(f'{path}/src/lib.rs').touch()
        
    return

def build_maturin_project(path: str | Path, release = False) -> None:
    
    """
    
    Build a maturin project in the given name of directory.
    Uses maturin build -> pip install pattern.
    
    Parameters:
        path: A str or a Path object that represents the project directory.
        release: Whether to use "--release" option when building.
        
    Errors:
        FileNotFoundError: Raised when there is no directory in the given path.
        CalledProcessError: Raised when maturin fails to build the project.
        ImportError: Raised when maturin does succeed to build the project, but pip fails to install the built wheels.
        
    """
    
    # Search for the directory under the current directory
    if not Path(str(path)).is_dir():
        raise FileNotFoundError(f"There is no directory on {Path(str(path)).resolve()}")
    
    # build
    recent_working_dir = os.getcwd()
    os.chdir(str(path))
    try:
        
        if release:
            run("maturin build --release")
        else:
            run("maturin build")
            
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(f"Maturin failed to build the project. \nPerhaps you forgot to initialize it? \nCaptured stderr call: \n{e.output}")
        
    try:
        run("pip install ./target/wheels/*")
    except subprocess.CalledProcessError as e:
        raise ImportError(f"Something went wrong when installing the wheel. \nCaptured stderr call: \n{e.output}")
        
    os.chdir(recent_working_dir)

    return 