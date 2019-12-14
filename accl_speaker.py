#後から埋める所はhatenaと記述してあります。
import smbus
import time
import pygame.mixer
get_time=[]


#music= ~.mp3
def play_sound(music):
    pygame.mixer.init() #init
    pygame.mixer.music.load(music) #read
    pygame.mixer.music.play(1) #do
    time.sleep(1)
    pygame.mixer.music.stop() #finish
    
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

xacc_list=[];yacc_list=[];zacc_list=[]
while True:
    data = bus.read_i2c_block_data(I2C_ADDR, 0x00, 7)

    xAccl = (data[1] * 256 + data[2]) / 16
    if xAccl > 2047 :
        xAccl -= 4096
    xacc_list.append(xAccl)

    yAccl = (data[3] * 256 + data[4]) / 16
    if yAccl > 2047 :
        yAccl -= 4096
    yacc_list.append(yAccl)

    zAccl = (data[5] * 256 + data[6]) / 16
    if zAccl > 2047 :
        zAccl -= 4096
    zacc_list.append(zAccl)

    #１回目の接地では音は鳴らない
    if xAccl<-1400 and yAccl>80:#接地条件by加速度
        time_pre=time.time()
        get_time.append(time_pre)
        if len(get_time)>2:
            print("time_diff={}".format(get_time[-1]-get_time[-2]))
            if get_time[-1]-get_time[-2]>3: #hatena2:閾値その１
                play_sound("./sound/zun.mp3") #hatena3:ぞうの足音とか
                
            elif get_time[-1]-get_time[-2]>2 and get_time[-1]-get_time[-2]<=3: #hatena4:閾値その２
                play_sound("./sound/pyuko.mp3") #hatena5:普通の足音
            else:
                play_sound("./sound/tetetete.mp3") #hatena6:てけてけ
                

    print("X,Y,Z-Axis : (%5d, %5d, %5d)" % (xAccl, yAccl, zAccl ))
    time.sleep(0.01)
