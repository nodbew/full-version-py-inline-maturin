import os
from pathlib import Path
from shutil import rmtree

import py_inline_maturin

def test_build():
    # Initialization of the working dir
    py_inline_maturin.initialize_maturin_project('maturin_test/pymodtest')
    py_inline_maturin.build_maturin_project('maturin_test/pymodtest')
    
    import pymodtest
    assert pymodtest.add_two(6) == 8
    assert type(pymodtest.split_string("hello ")) == list
    assert [t.strip() for t in pymodtest.split_string("Hello, world! I'm Macintosh.")] == ['Hello,', 'world!', "I'm", 'Macintosh.']
    rmtree("./pymodtest")

    return
