import subprocess, sys, tempfile, os
from typing import Tuple

def run_python_code(code: str, timeout: int = 30) -> Tuple[str, str]:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        tmp = f.name
    try:
        r = subprocess.run([sys.executable, tmp], capture_output=True, text=True, timeout=timeout)
        return r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        return "", f"TimeoutError: exceeded {timeout}s"
    except Exception as e:
        return "", str(e)
    finally:
        os.unlink(tmp)
