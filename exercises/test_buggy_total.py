"""修复前应出现 2 failed, 1 passed；不使用 xfail 掩盖错误。"""

import pytest

from exercises.buggy_total import total_energy


def test_all_devices_are_counted():
    assert total_energy([2.4, 0.3, 1.2]) == pytest.approx(3.9)


def test_one_device_is_counted():
    assert total_energy([2.4]) == pytest.approx(2.4)


def test_empty_list_is_zero():
    assert total_energy([]) == 0
