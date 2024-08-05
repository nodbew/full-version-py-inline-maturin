use pyo3::prelude::*;

#[pyfunction]
fn add_two(num: i64) -> i64 {
    num + 2
}

#[pyfunction]
fn split_string(s: &str) -> Vec<String> {
    s.split_whitespace().map(|part| part.to_string()).collect()
}

#[pymodule]
fn pymodtest(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add_two, m)?)?;
    m.add_function(wrap_pyfunction!(split_string, m)?)?;
    Ok(())
}