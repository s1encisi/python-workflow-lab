"""把测试临时文件放在项目内，便于在权限受限的环境中运行和观察。"""

import os


def pytest_configure(config):
    # 尊重调用者自己设置的临时目录。
    if config.option.basetemp or os.environ.get("PYTEST_DEBUG_TEMPROOT"):
        return
    temporary_root = config.rootpath / "artifacts" / "pytest-temp"
    temporary_root.mkdir(parents=True, exist_ok=True)
    os.environ["PYTEST_DEBUG_TEMPROOT"] = str(temporary_root)
