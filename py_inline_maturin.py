import subprocess
import os
from pathlib import Path

import toml

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
    
def initialize_maturin_project(name: str) -> None:
    '''
    Edit pyproject.toml and Cargo.toml in the directory, and change the directory into a maturin project.
    
    The following elements of the pyproject.toml file will be forecefully changed:
        - 'build-system' section: 'requires' will be 'maturin>=1.7, <2.0', 
                                  'build-backend' will be 'maurin'
        - 'project' section: 'features' will be ['pyo3/extension-module'] + other features if written.
                                  
    The following elements of the Cargo.toml file will be forecufully changed:
        - [lib]: 'crate-type' will be ['cdylib']
        - [dependencies]: 'pyo3' = { version = '0.22.0', features = ['extension-module'] }
    '''
    if not Path("./" + name).is_dir():
        raise FileNotFoundError("The directory does not exist")
    
    # Edit pyproject.toml
    try:
        config = toml.load(f'./{name}/pyproject.toml')
    except FileNotFoundError:
        # If there is no pyproject.toml, autogenerate the content
        config = toml.loads(f'''\
[project]
name = {name}
requires-python = ">=3.12"
classifiers = [
    "Programming Language :: Rust",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]
dynamic = ["version"]

[build-system]
requires = "maturin>=1.7, <2.0"
build-backend = "maturin"
''')
    if 'features' in config['project']:
        feats = config['project']['features']
        if 'pyo3/extension-module' not in feats:
            feats.append('pyo3/extension-module')
    else:
        config['project']['features'] = ['pyo3/extension-module']

    with open(f'./{name}/pyproject.toml', 'w') as f:
        toml.dump(config, f)

    # Edit Cargo.toml
    try:
        config = toml.load(f'./{name}/Cargo.toml')
    except FileNotFoundError:
        # Auto generation
        config = toml.loads(f'''\
[package]
name = {name}
version = "0.1.0"
edition = "2021"

[lib]
name = {name}
''')
    config['lib']['crate-type'] = ['cdylib']
    config['dependencies']['pyo3'] =  { "version": "0.22.0", "features": ["extension-module"] }

    with open(f'./{name}/Cargo.toml', 'w') as f:
        toml.dump(config, f)

    return

def build_maturin_project(path: str|Path) -> None:
    if not isinstance(path, (str, path)):
        raise TypeError(f'The "path" argument must be a str or pathlib.Path object, not {type(path)}')

    # Search for the directory under the current directory
    if not Path('./' + str(path)).is_dir():
        raise FileNotFoundError(f"There is no directory named {path}")

    # Develop
    os.chdir('./' + str(path))
    run(f"maturin build --verbose | pip install ./target/debug/maturin/{name}.whl")
    os.chdir('..')

    return 
