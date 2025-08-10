# lf_logger

一个简单易用的 Python 日志工具库。

## 功能简介
- 日志格式化
- 日志分级
- 实用工具函数

## 安装方法
```bash
pip install .
```

## 使用示例
```python
from lf_logger import logging
logger = logging.getLogger('my_logger')
logger.info('Hello, lf_logger!')
```

## 目录结构
```
lf_logger/
    __init__.py
    formatter.py
    logging.py
    utils.py
setup.py
```

## 许可证
MIT
