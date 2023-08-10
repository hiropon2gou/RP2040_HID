#main.py
is_debug = False
from machine import  Pin, SPI,UART, I2C,Timer,SoftI2C   
import utime  
import json
import sys
import time
import _thread
import micropython,os,sys
micropython.alloc_emergency_exception_buf(100)

import hid
sys.path.append('/ExternalLib')
sys.path.append('/Config')

from SN74LV8153 import SN74LV8153
from ADM489ABRZ import ADM489ABRZ
from CP2105 import CP2105 
from NAU7802 import NAU7802
from Singleton import Singleton
lock = _thread.allocate_lock()
config_param = None
timer_freq = 4
singleton = Singleton.getInstance()
singleton.set_time(time)
m_SN74LV8153 = SN74LV8153(machine,UART,Pin,utime,_thread)
m_SN74LV8153.set_number(8888,True,True)
singleton.load2flash()

m_NAU7802 = NAU7802(machine,I2C,Pin,time)
count = 0
timer_freq = 4
from button import button
m_button = button(machine,Pin,micropython,timer_freq)

m_is_max_value_mode = False
m_max_value = 0
m_is_Flashing = False
m_number = 0
offset = m_NAU7802.get_average_gram()

while True:
    count += 1    
    data = m_NAU7802.get_gram()
    force = data -offset
    if is_debug:
        print(data)
    if m_is_max_value_mode:
        if m_max_value < force:
            m_max_value = force
        m_number = m_max_value
    else:
        m_number = force
    if(abs(m_number)<=1):
        m_number = 0
    m_SN74LV8153.set_number(int(m_number),True,m_is_Flashing)
    x_axis = m_number / 750 * 127# -127
    if(x_axis > 127 and x_axis <= 127*2):
        x_axis += -127*2-1
    elif(x_axis > 127*2):
        x_axis = 127*2
    
    hid.send_hid_report(int(x_axis),0,0,0,0,0,1)
#    hid.send_hid_report(int(x_axis),int(y_axis),int(z_axis),int(rx_axis),int(ry_axis),int(rz_axis),1)
    if(m_button.is_push_ws1_flag):
        #reset offset
        offset = m_NAU7802.get_average_gram()
        m_max_value = 0
        m_button.is_push_ws1_flag = False
    if(m_button.is_push_ws2_flag):
        #toggle max value mode
        m_is_max_value_mode = not m_is_max_value_mode
        if m_is_max_value_mode:
            m_is_Flashing = True
            m_max_value = 0
        else:
            m_is_Flashing = False
        offset = m_NAU7802.get_average_gram()
        m_button.is_push_ws2_flag = False

    