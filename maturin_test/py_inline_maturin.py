import subprocess
import os
from pathlib import Path

import toml


class InvalidConfigError(Exception):pass
    

def run(cmd: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell = True, check = True, **kwargs)
    
def _edit_pyproject_toml(path: str, name: str) -> None:
    
    """
    The following elements of the pyproject.toml file will be forecefully changed:
        - 'build-system' section: 'requires' will be 'maturin>=1.7, <2.0' if omitted,
                                  'build-backend' will be 'maurin' if omitted
        - 'project' section: 'features' will be ['pyo3/extension-module'] + other features if written.
    """
    
    try:
        config = toml.load(path)
    except FileNotFoundError:
        # If there is no pyproject.toml, auto-generate the content
        config = toml.loads(f'''\
[project]
name = "{name}"
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

    # Check for invalid config files
    if 'project' not in config:
        raise InvalidConfigError('"project" section is required for pyproject.toml')

    # Edit configurations
    if 'features' in config['project']:
        feats = config['project']['features']
        if 'pyo3/extension-module' not in feats:
            feats.append('pyo3/extension-module')
    else:
        config['project']['features'] = ['pyo3/extension-module']

    if 'build-system' not in config:
        config['build-system'] = {'requires': 'maturin>=1.7, <2.0', 'build-backend': 'maturin'}
    else:
        if 'requires' not in config['build-system']:
            config['build-system']['requires'] = 'maturin>=1.7, <2.0'
        if 'build-backend' not in config['build-system']:
            config['build-system']['build-backend'] = 'maturin'

    with open(path, 'w') as f:
        toml.dump(config, f)
        
    return

def initialize_maturin_project(path: str, create: bool = False, name: str = None) -> None:
    '''
    Edit pyproject.toml and Cargo.toml to the maturin project style.
    
                                      
    The following elements of the Cargo.toml file will be forecufully changed:
        - [lib]: 'crate-type' will be ['cdylib']
        - [dependencies]: 'pyo3' = { version = '0.22.0', features = ['extension-module'] }
    '''

    # Name defaults to the directory name
    if name is None:
        name = str(path)
    
    if create:
        run(f"maturin new -b pyo3 ./{path}")
    else:
        if not Path(f"./{path}").exists():
            raise FileNotFoundError(f"The directory('{Path(f'./{path}').resolve()}') does not exist")

    _edit_pyproject_toml(path = f"./{path}/pyproject.toml", name = name)

    #
    # Edit Cargo.toml
    try:
        config = toml.load(f'./{name}/Cargo.toml')
    except FileNotFoundError:
        # Auto generation
        config = toml.loads(f'''\
[package]
name = "{name}"
version = "0.1.0"
edition = "2021"

[lib]
name = "{name}"

[dependencies]
''')
    # Check for required configurations
    for req in ['package', 'lib', 'dependencies']:
        if req not in config:
            raise InvalidConfigError(f'{req} section is required for Cargo.toml')
    
    config['lib']['crate-type'] = ['cdylib']
    config['dependencies']['pyo3'] =  { "version": "0.22.0", "features": ["extension-module"] }

    with open(f'./{name}/Cargo.toml', 'w') as f:
        toml.dump(config, f)

    # look for src directory
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
    

