"""只读显示本项目常用的环境信息，不打印凭据或全部环境变量。"""

import json
import platform
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    report = {
        "system": platform.system(),
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "virtual_environment": sys.prefix != sys.base_prefix,
        "project_root": str(PROJECT_ROOT),
        "working_directory": str(Path.cwd()),
        "in_project_root": Path.cwd() == PROJECT_ROOT,
        "tools_on_path": {
            name: shutil.which(name) for name in ("git", "docker", "uv", "code", "gh")
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
