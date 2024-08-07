# -*- coding: utf-8 -*-

import psutil
import time
import logging
from logging.handlers import RotatingFileHandler

# 设置日志输出路径和文件名
log_file_path = "/path/to/your/logfile.log"

# 配置日志
logging.basicConfig(
    handlers=[RotatingFileHandler(log_file_path, maxBytes=10**6, backupCount=3)],
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("CPULogger")

# 设置警告阈值，例如 90%
threshold = 90
# 设置持续时间，例如 5秒
duration = 5
# 设置检查间隔，例如 1秒
interval = 1

def check_cpu_usage():
    over_threshold_counts = [0] * psutil.cpu_count()

    while True:
        cpu_percentages = psutil.cpu_percent(interval=interval, percpu=True)
        for i, cpu_percent in enumerate(cpu_percentages):
            # 实时打印当前利用率，解除下行注释即可
            #logger.info(f"CPU 核心 {i} 当前利用率: {cpu_percent}%")
            print(f"CPU 核心 {i} 当前利用率: {cpu_percent}%")
            if cpu_percent > threshold:
                over_threshold_counts[i] += interval
                if over_threshold_counts[i] >= duration:
                    logger.warning(f"警告：CPU 核心 {i} 利用率持续 {duration} 秒超过 {threshold}%! 当前利用率: {cpu_percent}%")
                    print(f"警告：CPU 核心 {i} 利用率持续 {duration} 秒超过 {threshold}%! 当前利用率: {cpu_percent}%")
            else:
                over_threshold_counts[i] = 0

        time.sleep(interval)

if __name__ == "__main__":
    check_cpu_usage()
