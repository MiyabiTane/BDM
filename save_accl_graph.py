# -*- coding: utf-8 -*-
"""
加速度センサの値をリアルタイムで取得し、Ctrl+cで
プログラムを終了し、graphsディレクトリにグラフを保存する
詳しくは、READEME.mdを参照

"""
from __future__ import unicode_literals, print_function

import numpy as np
import matplotlib.pyplot as plt
import smbus
import time
import math

def pause_plot():
    x = [] #時間(x軸)を格納する空リストの作成
    y_x = [] #加速度センサのx軸の値(y軸)を格納する空リストの作成
    y_y = [] #加速度センサのy軸の値(y軸)を格納する空リストの作成
    y_z = [] #加速度センサのz軸の値(y軸)を格納する空リストの作成
    y_w = [] #加速度の大きさ(y軸)を格納する空リストの作成


    I2C_ADDR=0x1d #センサが入力されている場所の設定　場所は、i2cdetect -y 1 で確認

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

    #時間の初期化
    t=0



    # ここからCtrl+cまで無限にデータを取得し、リストに格納する
    try:
        while True:
            #時間の更新(ループは0.01秒で繰り返す)
            t+=0.01
            #加速度センサのデータを代入
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

            w = math.sqrt(xAccl**2 + yAccl**2 + zAccl**2) #加速度の大きさ

            #ｘの更新
            x.append(t)

            #加速度センサｘ軸の値の更新
            y_x.append(xAccl)

            #加速度センサy軸の値の更新
            y_y.append(yAccl)

            #加速度センサz軸の値の更新
            y_z.append(zAccl)


            #加速度の大きさの更新
            y_w.append(w)


            print("X,Y,Z-Axis : (%5d, %5d, %5d)" % (xAccl, yAccl, zAccl ))


            time.sleep(0.01) #この値によって、何秒に１回センサの値を取得するかが変わる　今は100Hz

    #Ctrl+cが押されたら、データの取得をやめ、グラフを作成し保存する
    except KeyboardInterrupt:
        fig=plt.figure(figsize=(10,10))
        plt.subplots_adjust(hspace=1)
        ax1 = plt.subplot(411)
        ax2 = plt.subplot(412)
        ax3 = plt.subplot(413)
        ax4 = plt.subplot(414)

        ax1.plot(x, y_x, color="red")
        ax1.set_xlim(min(x), max(x))
        ax1.set_ylim(min(y_x)-10, max(y_x)+10)
        ax1.set_title("acceleration x-axis")

        ax2.plot(x, y_y, color="blue")
        ax2.set_xlim(min(x), max(x))
        ax2.set_ylim(min(y_y)-10, max(y_y)+10)
        ax2.set_title("acceleration y-axis")

        ax3.plot(x, y_z, color="green")
        ax3.set_xlim(min(x), max(x))
        ax3.set_ylim(min(y_z)-10, max(y_z)+10)
        ax3.set_title("acceleration z-axis")

        ax4.plot(x, y_z, color="black")
        ax4.set_xlim(min(x), max(x))
        ax4.set_ylim(0, max(y_w)+10)
        ax4.set_title("the magnitude of the acceleration")

        fig.savefig("graphs/accl_graph.png") #必要に応じてファイル名は変える

        #処理が終わったこと、それぞれの最大値、最小値を表示
        print(" done!")
        print("the graph is saved")
        print("the max of x-axis acceleration is %5d" % max(y_x))
        print("the min of x-axis acceleration is %5d" % min(y_x))
        print("the max of y-axis acceleration is %5d" % max(y_y))
        print("the min of y-axis acceleration is %5d" % min(y_y))
        print("the max of z-axis acceleration is %5d" % max(y_z))
        print("the min of z-axis acceleration is %5d" % min(y_z))
        print("the max of the magnitude of the acceleration is %5d" % max(y_w))

if __name__ == "__main__":
    pause_plot()
