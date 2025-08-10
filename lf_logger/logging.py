import logging
import os
from argparse import Namespace
from collections.abc import Iterable, Sized
from pathlib import Path
import sys
import time
import typing as tp

from .utils import AnyPath

import colorlog
from .formatter import Formatter

default_log_name="my_logger"  #log_name不可以是__file__会出问题的

class MyLogger(logging.Logger):

    LogDirPath:str ="./logs"

    _instance: tp.Optional["MyLogger"] = None
    def __new__(cls,*args, **kwargs)->"MyLogger":
        if cls._instance==None:
            cls._instance=super().__new__(cls)

        return cls._instance
    


    def __init__(self,log_name:str,log_level: int =logging.DEBUG) ->None:
        super().__init__(log_name)
        # 创建一个日志器logger并设置其日志级别为DEBUG
  
        log_colors_config = {
        'DEBUG': 'white',  # cyan white
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
        }
        self.setLevel(log_level)

        # 创建一个流处理器handler并设置其日志级别为DEBUG
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)

        file_formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] [%(filename)s -> %(funcName)s] [line:%(lineno)d] [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S'

        )
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] [%(filename)s -> %(funcName)s] [line:%(lineno)d] [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=log_colors_config
        )


        # 创建一个格式器formatter并将其添加到处理器handler
       # formatter = logging.Formatter('[%(asctime)s %(name)s %(filename)s [line:%(lineno)d]] %(levelname)s %(message)s')
        console_handler.setFormatter(console_formatter)
        

        dir_path=Path(self.LogDirPath)
        if not dir_path.exists():
            os.mkdir(self.LogDirPath)
        

        log_path= dir_path / f"{log_name}.log"
        # 创建一个文件处理器handler并设置其日志级别为DEBUG
        file_handler = logging.FileHandler(filename=log_path,mode='a')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)


        # 为日志器logger添加上面创建的处理器handler
        self.addHandler(console_handler)
        self.addHandler(file_handler) 

    def setLevel(self, level: tp.Union[int ,str]) -> None:
        return super().setLevel(level)

# logger=MyLogger("my_logger")




def setup_logging(
        log_name: str = 'my_logger',
        level: int = logging.INFO,
        folder: tp.Optional[AnyPath] = './logs',
        with_file_log: bool = True,
        
):
    """Setup logging nicely, we recommend you call this as the very first step,
    not to miss any possible messages. By default this will also create a log file in the experiment folder.

    Args:
        with_file_log: if True, creates a log file in the XP folder,
            or the folder given explicitely. Default is True.
        folder: customize folder to store the logs in.
        log_name: template for the filename of the log. Default is
            `solver.log.{rank}`.
        level: log level, default is `logging.INFO`.
    """
    # See https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook for reference.
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    sh = logging.StreamHandler(sys.stderr)
    sh.setLevel(level)

    # Let us switch to colorlog for an improved esthetic experience.
    log_format = ('[%(cyan)s%(asctime)s%(reset)s][%(blue)s%(name)s%(reset)s]'
                  '[%(log_color)s%(levelname)s%(reset)s] - %(message)s')
    formatter = colorlog.ColoredFormatter(
        log_format,
        datefmt="%m-%d %H:%M:%S")

    sh = logging.StreamHandler(sys.stderr)
    sh.setLevel(level)
    sh.setFormatter(formatter)
    root_logger.addHandler(sh)

    if with_file_log:
        if folder is None:
            folder = './logs'
        folder_path = Path(folder)
        folder_path.mkdir(parents=True, exist_ok=True)  # 确保目录存在
        filename = f'{log_name}.log'
        fh = logging.FileHandler(folder_path / filename)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        root_logger.addHandler(fh)