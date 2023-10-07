# -*- coding: utf-8 -*-
from tuning import Tuning
import usb.core
import usb.util
import time
import statistics  # 导入统计模块

# 定义收集数据的时间间隔和采样次数
collection_interval = 0.1  # 数据采集间隔（秒）
samples_per_average = 20  # 每次计算平均值的样本数

# 定义异常值的标准差倍数
std_dev_multiplier = 2  # 根据需要调整标准差倍数

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

if dev:
    Mic_tuning = Tuning(dev)
    doa_samples = []  # 存储DOA角度样本的列表

    while True:
        try:
            # 读取DOA角度并添加到样本列表中
            doa_angle = Mic_tuning.direction
            doa_samples.append(doa_angle)

            if len(doa_samples) >= samples_per_average:
                # 计算标准差
                std_dev = statistics.stdev(doa_samples)

                # 去除超过标准差倍数的异常点
                filtered_samples = [angle for angle in doa_samples if abs(angle - doa_angle) <= std_dev_multiplier * std_dev]

                if filtered_samples:
                    # 计算剩余数据的平均值并输出（取整）
                    avg_doa_angle = int(sum(filtered_samples) / len(filtered_samples))
                    print(avg_doa_angle)
                else:
                    print("No valid data collected.")

                # 清空样本列表
                doa_samples = []

            time.sleep(collection_interval)

        except KeyboardInterrupt:
            break

else:
    print("USB device not found.")
