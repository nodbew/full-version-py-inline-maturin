from pathlib import Path

import py_inline_maturin

def test_create():
    """Test creation of a project"""
    
    py_inline_maturin.initialize_maturin_project("something", create = True)
    assert Path("./something").is_dir()
    assert Path("./something/Cargo.toml").is_file()
    assert Path("./something/pyproject.toml").is_file()
    assert Path("./something/src").is_dir()
    assert Path("./something/src/lib.rs").is_file()
    
    return
    
def test_initialization():
    Path("./some_maturin_proj").mkdir()
    py_inline_maturin.initialize_maturin_project("some_maturin_proj")
    assert Path("./some_maturin_proj/Cargo.toml").is_file()
    assert Path("./some_maturin_proj/pyproject.toml").is_file()
    assert Path("./some_maturin_proj/src").is_dir()
    assert Path("./some_maturin_proj/src/lib.rs").is_file()
    
    return
    
def test_created_dir_build():
    py_inline_maturin.initialize_maturin_project("test_maturin_project", create = True)
    with open("./test_maturin_project/src/lib.rs", "w", encoding = "utf-8") as f:
        f.write("""\
use pyo3::prelude::*;

#[pymodule]
mod test_maturin_project {

    use pyo3::prelude::*;
    
    #[pyfunction]
    fn subtract_two(n: i64) -> i64 {
        n - 2
    }
    
}
""")
    py_inline_maturin.build_maturin_project("test_maturin_project")
    import test_maturin_project
    assert test_maturin_project.subtract_two(4) == 2
    
    return
    
def test_manual_written_build():
    py_inline_maturin.build_maturin_project('maturin_test/pymodtest')
    
    import pymodtest
    assert pymodtest.add_two(6) == 8
    assert type(pymodtest.split_string("hello ")) == list
    assert [t.strip() for t in pymodtest.split_string("Hello, world! I'm Macintosh.")] == ['Hello,', 'world!', "I'm", 'Macintosh.']

    return
    
def test_initialized_project_build():
    # Initialization of the project directory
    py_inline_maturin.initialize_maturin_project('maturin_test/pymodtest')
    py_inline_maturin.build_maturin_project('maturin_test/pymodtest')
    
    import pymodtest
    assert pymodtest.add_two(6) == 8
    assert type(pymodtest.split_string("hello ")) == list
    assert [t.strip() for t in pymodtest.split_string("Hello, world! I'm Macintosh.")] == ['Hello,', 'world!', "I'm", 'Macintosh.']

    return
