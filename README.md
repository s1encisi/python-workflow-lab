# Python Workflow Lab

以设备用电计算器为例的 Python 工程练习项目：模块划分、命令行入口、异常处理、测试、代码检查与开发容器配置。

## 运行

```bash
python -m venv .venv
# 激活虚拟环境后：
python -m pip install -r requirements-dev.txt
python main.py
python -m pytest -q
```

业务代码只依赖 Python 标准库。`energy_lab/` 为核心模块，`tests/` 为默认测试，`exercises/` 包含有意设置错误的独立练习。输入数据为虚构示例，不代表真实设备记录或电价。
