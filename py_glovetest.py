#python -m pip install numpy & pynput 安装插件包
#python -m pip install upgrade pip   升级pip
#本目录使用32位的WISEGLOVE.DLL程序

from ctypes import *
import time
import ctypes
import sys, os
from pynput.keyboard import Controller,Key,Listener
from pynput import keyboard
import keyboard
import numpy as np
import msvcrt
lib = CDLL("./WISEGLOVEU3D.dll")

global disp
disp=ctypes.c_int
g_pGlove=ctypes.c_bool
num_sensor = ctypes.c_int #初始化传感器数量
#sn = (c_char_p * 32)()

snfunc = lib.wgGetSn
snfunc.restype = ctypes.c_bool # 设置返回值类型
snfunc.argtypes = [ctypes.POINTER(ctypes.c_char)] # 设置参数类型

angle=(c_float*15)()
sensor=(c_ushort*15)()

disp =1
timestamp=ctypes.c_uint


print ("Press q to exit this program!")
print ("Press s to show sensor value!")
print ("Press a to show angle!")
print ("Press r to zero angle!")


lib.wgInit.restype = ctypes.c_bool
#g_pGlove=lib.wgInitManu(3,115200)
g_pGlove=lib.wgInit(-1)  #0=左手,1=右手,－1=不分左右 

if g_pGlove==False:
        print("请插上数据手套")
        lib.wgClose()
else:
        
        lib.wgGetNumOfSensor.restype = ctypes.c_int
        num_sensor=lib.wgGetNumOfSensor()
        print("数据手套已成功连接！")
        print("该数据手套角度传感器的个数:%d"%num_sensor)
        #lib.wgGetSn(sn)
        sn_str = b'aaaaaaaaa' # 转换为bytes格式
        snfunc(sn_str)
        print(sn_str)
        
#lib.wgSetCalibMode(ctypes.c_int(0))#自动标定

#打印手指各关节标签：拇指MCP(01),IP(02),拇指食指(03),食指MCP-PIP(04,05),食指中指(06),中指MCP-DIP(07,08),
#                  中指环指(09),环指MCP-DIP(10,11),环指小指(12),小指MCP-DIP(13,14)
for i in range (num_sensor):
        print ("第%s个\t" %(i+1) ,end="")
print('\n')

while 1:
        if msvcrt.kbhit():
                key=msvcrt.getch()
                #print(type(key))
                keystr=str(key, encoding="utf-8")
                if (keystr=='q'):
                        break
                if (keystr=='a'):
                        disp=1
                        print("disp==1")
                if (keystr=='s'):
                        disp=0
                        print("disp=0")
                if (keystr=='r'):
                        lib.wgResetCalib()
        if disp==1:
                lib.wgGetAngle.restype = ctypes.c_uint
                timestamp=lib.wgGetAngle(angle)
                if timestamp>0:
                        for i in range (num_sensor):
                                print("%.1f\t" %angle[i],end="")
                        print ('\n',end='')
        if disp==0:
                lib.wgGetData.restype = ctypes.c_uint
                timestamp=lib.wgGetData(sensor)
                if timestamp>0:
                        for i in range (num_sensor):
                                print("%04d\t" %sensor[i],end="")
                        print ('\n',end='')
        time.sleep(0.01)
lib.wgClose()

