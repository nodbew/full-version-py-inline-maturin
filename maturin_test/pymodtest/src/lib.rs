use pyo3::prelude::*;

#[pyfunction]
fn add_two(num: i64) -> PyResult<i64> {
    Ok(num + 2)
}

#[pyfunction]
fn split_string(s: &str) -> PyResult<Vec<String>> {
    Ok(s.split_whitespace().map(|part| part.to_string()).collect())
}

#[pymodule]
fn pymodtest(m: &Bound<'_, PyModule>) -> PyResult<()> {
    println!("{:?}", m.add_function(wrap_pyfunction!(add_two, m)?));
    println!("{:?}", m.add_function(wrap_pyfunction!(split_string, m)?)?);
    Ok(())
}