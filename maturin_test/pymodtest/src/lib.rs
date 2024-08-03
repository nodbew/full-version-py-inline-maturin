use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
pub fn add_two(num: i64) -> i64 {
    num + 2
}

#[pyfunction]
pub fn split_string(s: &str) -> Vec<String> {
    s.split_whitespace().map(|part| part.to_string()).collect()
}

#[pymodule]
#[pyo3(name="pymodtest")]
fn pymodtest(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add_two, m)?)?;
    m.add_function(wrap_pyfunction!(split_string, m)?)?;
    Ok(())
}