import math

import pytest

from energy_lab.calculator import build_report, calculate_cost, energy_kwh


@pytest.mark.parametrize(
    ("power_w", "hours", "expected"),
    [(1000, 1, 1), (1200, 2, 2.4), (60, 5, 0.3), (0, 5, 0), (800, 0, 0)],
)
def test_energy_conversion(power_w, hours, expected):
    assert energy_kwh(power_w, hours) == pytest.approx(expected)


@pytest.mark.parametrize("bad_value", [-1, math.nan, math.inf, "1000", True, None])
@pytest.mark.parametrize("field", ["power_w", "hours"])
def test_bad_measurements_are_rejected(bad_value, field):
    values = {"power_w": 1000, "hours": 2}
    values[field] = bad_value
    with pytest.raises(ValueError, match=field):
        energy_kwh(**values)


def test_overflow_is_rejected():
    with pytest.raises(ValueError):
        energy_kwh(1e308, 1e308)


def test_cost_is_rounded_to_two_decimals():
    assert calculate_cost(1.234, 0.8) == 0.99


@pytest.mark.parametrize("bad_price", [-0.1, math.nan, math.inf, "0.8", True])
def test_bad_prices_are_rejected(bad_price):
    with pytest.raises(ValueError, match="price"):
        calculate_cost(1, bad_price)


def test_report_contains_independent_expected_totals():
    devices = [
        {"name": "heater", "power_w": 1200, "hours": 2},
        {"name": "lamp", "power_w": 60, "hours": 5},
        {"name": "pump", "power_w": 800, "hours": 1.5},
    ]
    report = build_report(devices, price=0.8)
    assert [row["name"] for row in report["devices"]] == ["heater", "lamp", "pump"]
    assert report["total_kwh"] == pytest.approx(3.9)
    assert report["total_cost"] == 3.12
    assert "kwh" not in devices[0]  # 生成报告不能修改原始输入。


def test_empty_report_is_zero():
    report = build_report([])
    assert report["devices"] == []
    assert report["total_kwh"] == 0
    assert report["total_cost"] == 0


@pytest.mark.parametrize(
    "devices",
    [
        {},
        ["heater"],
        [{"name": "heater"}],
        [{"name": "  ", "power_w": 1000, "hours": 1}],
        [{"name": 42, "power_w": 1000, "hours": 1}],
    ],
)
def test_invalid_data_shape_is_rejected(devices):
    with pytest.raises(ValueError):
        build_report(devices)
