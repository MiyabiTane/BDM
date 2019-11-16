# -*- coding: utf-8 -*-
"""
matplotlibでリアルタイムプロットする例

無限にsin関数をplotし続ける
"""
from __future__ import unicode_literals, print_function

import numpy as np
import matplotlib.pyplot as plt
import smbus
import time

def pause_plot():
    plt.figure(figsize=(10,8))
    plt.subplots_adjust(hspace=1)
    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312)
    ax3 = plt.subplot(313)
    x = [-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0] #np.arange(-1, 1, 0.1)
    y_x = [0,0,0,0,0,0,0,0,0,0] #np.sin(x)
    y_y = [0,0,0,0,0,0,0,0,0,0]
    y_z = [0,0,0,0,0,0,0,0,0,0]
    ax1.set_xlim(-1, 0)
    ax1.set_ylim(-1, 1)
    ax2.set_xlim(-1, 0)
    ax2.set_ylim(-1, 1)
    ax3.set_xlim(-1, 0)
    ax2.set_ylim(-1, 1)
    # 初期化的に一度plotしなければならない
    # そのときplotしたオブジェクトを受け取る受け取る必要がある．
    # listが返ってくるので，注意
    lines1, = ax1.plot(x, y_x, color="red")
    ax1.set_title("acceleration x-axis")

    lines2, = ax2.plot(x, y_y, color="blue")
    ax2.set_title("acceleration y-axis")

    lines3, = ax3.plot(x, y_z, color="green")
    ax3.set_title("acceleration z-axis")

    I2C_ADDR=0x1d

    # Get I2C bus
    bus = smbus.SMBus(1)

    # Select Control register, 0x2A(42)
    #               0x00(00)        StandBy mode
    bus.write_byte_data(I2C_ADDR, 0x2A, 0x00)

    # Select Control register, 0x2A(42)
    #               0x01(01)        Active mode
    bus.write_byte_data(I2C_ADDR, 0x2A, 0x01)

    # Select Configuration register, 0x0E(14)
    #               0x00(00)        Set range to +/- 2g
    bus.write_byte_data(I2C_ADDR, 0x0E, 0x00)

    time.sleep(0.5)


    # ここから無限にplotする
    while True:
        # plotデータの更新
        data = bus.read_i2c_block_data(I2C_ADDR, 0x00, 7)
        xAccl = (data[1] * 256 + data[2]) / 16
        if xAccl > 2047 :
            xAccl -= 4096
        yAccl = (data[3] * 256 + data[4]) / 16
        if yAccl > 2047 :
            yAccl -= 4096
        zAccl = (data[5] * 256 + data[6]) / 16
        if zAccl > 2047 :
            zAccl -= 4096


        x = map(lambda p: p+0.1, x)
        y_x.pop(0)
        y_x.append(xAccl)

        lines1.set_data(x, y_x)
        ax1.set_xlim(min(x), max(x))
        ax1.set_ylim(min(y_x)-10, max(y_x)+10)


        y_y.pop(0)
        y_y.append(yAccl)

        lines2.set_data(x, y_y)
        ax2.set_xlim(min(x), max(x))
        ax2.set_ylim(min(y_y)-10, max(y_y)+10)


        y_z.pop(0)
        y_z.append(zAccl)

        lines3.set_data(x, y_z)
        ax3.set_xlim(min(x), max(x))
        ax3.set_ylim(min(y_z)-10, max(y_z)+10)



        # set_data()を使うと軸とかは自動設定されないっぽいので，
        # 今回の例だとあっという間にsinカーブが描画範囲からいなくなる．
        # そのためx軸の範囲は適宜修正してやる必要がある．
        #ax.set_xlim(x-1, x)

        # 一番のポイント
        # - plt.show() ブロッキングされてリアルタイムに描写できない
        # - plt.ion() + plt.draw() グラフウインドウが固まってプログラムが止まるから使えない
        # ----> plt.pause(interval) これを使う!!! 引数はsleep時間
        time.sleep(0.1)
        plt.pause(.01)

if __name__ == "__main__":
    pause_plot()
