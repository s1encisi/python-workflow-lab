"""演示临时目录自动清理；临时目录本身不提供安全隔离。"""

from pathlib import Path
from tempfile import TemporaryDirectory


def main() -> None:
    with TemporaryDirectory(prefix="energy-lab-") as directory:
        report = Path(directory) / "example.txt"
        report.write_text("This is a disposable practice file.\n", encoding="utf-8")
        print(f"Temporary file: {report}")
        print(f"Exists inside the with block: {report.exists()}")  # 可在这里打断点。
        print(report.read_text(encoding="utf-8").strip())
    print(f"Exists after leaving the with block: {report.exists()}")
    print("Cleanup is not a security boundary; this Python process has your permissions.")


if __name__ == "__main__":
    main()
