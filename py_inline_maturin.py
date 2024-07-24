import subprocess
from pathlib import Path
import os

def run(cmd: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell = True, check = True, **kwargs)

def create_maturin_project(name: str) -> None:
    '''
    Create a new maturin project with the desired name.
    '''

    if type(name) != str:
        raise TypeError(f'The "name" argument must be a str instance, not {type(name)}')
        
    # Check overlappings
    if Path('./' + name).is_dir():
        raise FileExistsError(f"Directory {name} already exists; please choose another name")

    # Install rust and maturin
    run("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
    print('Successfully installed rust:')
    run("rustup --version")
    run("pip install -U maturin")

    # Maturin new
    run(f"maturin new --name {name} --bindings pyo3 ./{name}")
    
    return 

def build_maturin_project(path: str|Path) -> None:
    if not isinstance(path, (str, path)):
        raise TypeError(f'The "path" argument must be a str or pathlib.Path object, not {type(path)}')

    # Search for the directory under the current directory
    if not Path('./' + str(path)).is_dir():
        raise FileNotFoundError(f"There is no directory named {path}")

    # Develop
    os.chdir('./' + str(path))
    run("maturin build --verbose")
    os.chdir('..')

    return 
