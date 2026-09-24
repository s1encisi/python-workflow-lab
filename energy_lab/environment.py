"""只打印与本练习相关的环境信息，用来对比 Windows、WSL 和容器。"""

import json
import os
import platform
import sys
from pathlib import Path


def environment_info() -> dict:
    release = platform.release()
    return {
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "system": platform.system(),
        "kernel_release": release,
        "working_directory": str(Path.cwd()),
        "virtual_environment": sys.prefix != sys.base_prefix,
        "python_prefix": sys.prefix,
        "python_base_prefix": sys.base_prefix,
        "wsl_hint": "microsoft" in release.lower(),
        "container_hint": Path("/.dockerenv").is_file(),
        "LAB_RUN_MODE": os.environ.get("LAB_RUN_MODE", "terminal"),
    }


if __name__ == "__main__":
    print(json.dumps(environment_info(), ensure_ascii=False, indent=2))
