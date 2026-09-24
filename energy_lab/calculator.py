"""计算设备用电量；这里最适合练习断点、单步进入和单元测试。"""

import logging
import math

logger = logging.getLogger(__name__)


def validate_number(value: float, name: str) -> None:
    """本练习只接受有限的非负数，避免负值、NaN 和无穷大混入结果。"""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and non-negative")


def energy_kwh(power_w: float, hours: float) -> float:
    """用电量（kWh）= 功率（W）× 时间（h）÷ 1000。"""
    validate_number(power_w, "power_w")
    validate_number(hours, "hours")
    result = power_w / 1000 * hours  # 断点 B：观察输入怎样变成输出。
    validate_number(result, "energy_kwh")
    return result


def calculate_cost(kwh: float, price: float) -> float:
    """按统一单价估算费用；课堂示例，不包含真实电价政策。"""
    validate_number(kwh, "kwh")
    validate_number(price, "price")
    cost = kwh * price
    validate_number(cost, "cost")
    return round(cost, 2)


def build_report(devices: list[dict], price: float = 0.8) -> dict:
    """生成明细和汇总。零设备返回零用电、零费用。"""
    validate_number(price, "price")
    if not isinstance(devices, list):
        raise ValueError("devices must be a JSON list")

    rows = []
    for device in devices:
        if not isinstance(device, dict):
            raise ValueError("each device must be a JSON object")
        required = {"name", "power_w", "hours"}
        if not required <= device.keys():
            raise ValueError("each device needs name, power_w and hours")
        if not isinstance(device["name"], str) or not device["name"].strip():
            raise ValueError("device name must be a non-empty string")
        kwh = energy_kwh(device["power_w"], device["hours"])  # 断点 A：按 F11。
        logger.debug("device=%s, energy=%.3f kWh", device["name"], kwh)
        rows.append({"name": device["name"], "kwh": kwh})

    total_kwh = math.fsum(row["kwh"] for row in rows)
    return {
        "devices": rows,
        "total_kwh": total_kwh,
        "price": price,
        "total_cost": calculate_cost(total_kwh, price),
    }
