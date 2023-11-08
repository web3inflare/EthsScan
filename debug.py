# """
# @Time ： 2023/11/1 23:56
# @Auth ： Web3inFlare
# @File ：debug.py
# @IDE ：PyCharm
# @Motto: 咕咕嘎嘎
# """
import time
from loguru import logger
t = time.strftime("%Y-%m-%d")
logger.add(f"Output_{t}.log",
           rotation="100 MB",  # 最大保存大小
           encoding="utf-8",  # 支持中文格式
           enqueue=True,  # 支持异步存储
           retention=10000,  # 保存期限10天
           )
