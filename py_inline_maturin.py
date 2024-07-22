import subprocess
from pathlib import Path

def create_new_maturin(name: str|Path) -> bool:
    if Path(str(name)).is_dir:
        raise FileExistsError(f"Directory {name} already exists; please choose another name")
    
    subprocess.run("pip install -U maturin", shell = True)
    subprocess.run(f"maturin init {name}")
    return True