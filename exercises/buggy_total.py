"""故意保留一个 bug。先运行配套测试，再用调试器找到原因。"""


def total_energy(readings: list[float]) -> float:
    """需求：把所有设备的用电量相加；空列表应返回 0。"""
    total = 0.0
    for index in range(len(readings) - 1):  # 调试时观察 index 和 len(readings)。
        total += readings[index]
    return total


if __name__ == "__main__":
    sample = [2.4, 0.3, 1.2]
    actual = total_energy(sample)
    print(f"Input: {sample}")
    print(f"Actual: {actual:.1f} kWh; expected: 3.9 kWh")
