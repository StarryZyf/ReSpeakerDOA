# -*- coding: utf-8 -*-
from tuning import Tuning
import usb.core
import usb.util
import time

# 定义收集数据的时间间隔和采样次数
collection_interval = 0.1  # 数据采集间隔（秒）
samples_per_average = 10  # 每次计算平均值的样本数

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

if dev:
    Mic_tuning = Tuning(dev)
    doa_samples = []  # 存储DOA角度样本的列表
    sample_count = 0

    while True:
        try:
            # 读取DOA角度并添加到样本列表中
            doa_angle = Mic_tuning.direction
            doa_samples.append(doa_angle)
            sample_count += 1

            if sample_count >= samples_per_average:
                # 计算DOA角度的平均值并输出
                if doa_samples:
                    avg_doa_angle = sum(doa_samples) / len(doa_samples)
                    print(avg_doa_angle)
                else:
                    print("No data collected.")

                # 重置样本列表和计数
                doa_samples = []
                sample_count = 0

            time.sleep(collection_interval)

        except KeyboardInterrupt:
            break

else:
    print("USB device not found.")

