import os
from pathlib import Path
from shutil import rmtree

import pytest

import py_inline_maturin

def test_creation():
    current_directory = os.getcwd()
    py_inline_maturin.create_maturin_project(name = "creation_test")
    if os.getcwd() != current_directory:
        raise ValueError("Current directory changed")
    if not Path('./creation_test').exists():
        raise FileNotFoundError("The directory wasn't successfully created")

    # Clean up
    rmtree('./creation_test')
    
    return

# Test function
def test_build():
    # Initialization of the working dir
    py_inline_maturin.initialize_maturin_project('pymodtest')
        
    py_inline_maturin.build_maturin_project('pymodtest')
    import pymodtest
    
    import subprocess
    subprocess.run("sudo apt-get install tree", shell = True, check = True)
    subprocess.run("tree ./pymodtest", shell = True, check = True)
    raise Exception()
    
    assert pymodtest.add_two(6) == 8
    assert type(pymodtest.split_string("hello ")) == list
    assert [t.strip() for t in pymodtest.split_string("Hello, world! I'm Macintosh.")] == ['Hello,', 'world!', "I'm", 'Macintosh.']
    
    rmtree("./pymodtest")

    return