"""同一个检查入口可在 Windows、WSL 或 Dev Container 中使用。"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    commands = [
        [sys.executable, "-m", "ruff", "check", "."],
        [sys.executable, "-m", "ruff", "format", "--check", "."],
        [sys.executable, "-m", "pytest", "tests", "-q"],
    ]
    for command in commands:
        print("\n> " + " ".join(command), flush=True)
        result = subprocess.run(command, cwd=PROJECT_ROOT, check=False)
        if result.returncode:
            return result.returncode
    print("\nAll checks passed. Intentional exercises are checked separately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
