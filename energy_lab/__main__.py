"""命令行入口：在项目根目录执行 python -m energy_lab。"""

import argparse
import json
import logging
from pathlib import Path

from energy_lab.calculator import build_report

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Calculate a small electricity report")
    parser.add_argument("--data", type=Path, default=PROJECT_ROOT / "data" / "devices.json")
    parser.add_argument("--price", type=float, default=0.8, help="price per kWh (default: 0.8)")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    parser.add_argument("--verbose", action="store_true", help="show DEBUG logs")
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    try:
        devices = json.loads(args.data.read_text(encoding="utf-8"))
        report = build_report(devices, args.price)
    except (OSError, ValueError, OverflowError) as exc:
        # 在 VS Code 勾选 Raised Exceptions，可在异常被这里捕获前停住。
        parser.exit(2, f"Input error: {exc}\n")

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    else:
        print("Electricity report (synthetic learning data)")
        for row in report["devices"]:
            print(f"  {row['name']:<12} {row['kwh']:.3f} kWh")
        print(f"Total energy: {report['total_kwh']:.3f} kWh")
        print(f"Unit price:   {report['price']:.2f} yuan/kWh")
        print(f"Total cost:   {report['total_cost']:.2f} yuan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
