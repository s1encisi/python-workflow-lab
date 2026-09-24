"""仅供教学 Docker 沙箱运行，观察文件权限、网卡和资源上限。"""

import os
import socket
from pathlib import Path


def main() -> int:
    if os.environ.get("LAB_SANDBOX") != "1" or not Path("/.dockerenv").exists():
        print("Run this probe with the sandbox command in docs/04-environments.md.")
        return 2

    print(f"User ID: {os.getuid()}")
    for destination in (Path("/app/probe-output.txt"), Path("/tmp/probe-output.txt")):
        try:
            destination.write_text("sandbox exercise\n", encoding="utf-8")
            print(f"WRITE OK: {destination}")
        except OSError as exc:
            print(f"WRITE BLOCKED: {destination} ({exc.strerror})")

    print(f"Network interfaces: {socket.if_nameindex()}")
    for name in ("memory.max", "pids.max", "cpu.max"):
        path = Path("/sys/fs/cgroup") / name
        value = path.read_text(encoding="utf-8").strip() if path.exists() else "not cgroup v2"
        print(f"{name}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
