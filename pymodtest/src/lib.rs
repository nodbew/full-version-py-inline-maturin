use pyo3::prelude::*;

#[pyfunction]
pub fn add_two(num: i64) -> i64 {
    num + 2
}

#[pyfunction]
pub fn split_string(s: &str) -> Vec<&str> {
    let mut result = vec![];
    for part in s.split_whitespace() {
        result.push(part);
    }
    result
}

#[pymodule]
pub fn pymodtest(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add_two, m)?)?;
    m.add_function(wrap_pyfunction!(split_string, m)?)?;
    Ok(())
}