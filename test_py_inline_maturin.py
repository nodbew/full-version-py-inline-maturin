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

@pytest.mark.parametrize(('cmd',), [
    ('''
use pyo3::prelude::*;

#[pyfunction]
fn add_two(num: i64) -> i64 {
    num + 2
}

#[pymodule]
fn test_mod(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add_two, m)?)?;
    Ok(())
}
    ''',),
    ('''
use pyo3::prelude::*;

#[pyfunction]
fn split_string(s: &str) -> Vec<&str> {
    let mut result = vec![];
    for part in s.split_whitespace() {
        result.push(part);
    }
    result
}

#[pymodule]
fn test_mod(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(split_string, m)?)?;
    Ok(())
}
    ''',),
])
def test_build(cmd):
    
    if Path('./pymodtest').is_dir():
        import warnings
        import subprocess
        warnings.warn("Found pymondtest. Here is the tree of the directory:\n")
        subprocess.run(r'find . | sed -e "s/[^-][^\/]*\// |/g" -e "s/|\([^ ]\)/|-\1/', shell=True, check=True)
        subprocess.run("bash stdout_and_stderr.sh > stderr.log")
        rmtree('./pymodtest')

    py_inline_maturin.create_maturin_project('pymodtest')
    with open('./pymodtest/src/lib.rs', 'w', encoding = 'utf-8') as f:
        f.write(cmd)
    py_inline_maturin.build_maturin_project('pymodtest')
    import test_mod
    try:
        assert test_mod.add_two(6) == 8
    except NameError:
        assert type(test_mod.split_string("hello ")) == list
        assert [t.strip() for t in test_mod.split_string("Hello, world! I'm Macintosh.")] == ['Hello,', 'world!', "I'm", 'Macintosh.']

    # Clean up
    rmtree('./pymodtest')
    
    return
