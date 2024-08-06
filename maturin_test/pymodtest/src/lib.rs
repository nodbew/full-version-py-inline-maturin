use pyo3::prelude::*;

#[pymodule]
mod pymodtest {
    
    use pyo3::prelude::*;
    
    #[pyfunction]
    fn add_two(num: i64) -> i64 {
        num + 2
    }
    
    #[pyfunction]
    fn split_string(s: &str) -> Vec<String> {
        s.split_whitespace()
            .map(|part| part.to_string())
            .collect()
    }
    
}