#CP2105.py

from machine import Pin, SPI,UART, I2C,Timer   
import utime  
import json
import sys
import time
import _thread
import micropython,os,sys
res_message = bytearray(100)
class CP2105():
    def __init__(self,time,machine,UART,Pin):
        self.time = time
        self.uart0 = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9),rts=Pin(11),cts=Pin(10),flow =UART.RTS | UART.CTS)
        self.CP2105_GPIO1 = machine.Pin(7,machine.Pin.OUT)
        self.CP2105_GPIO0 = machine.Pin(6,machine.Pin.OUT)
        self.CP2105_DCD_ECI = machine.Pin(5,machine.Pin.OUT)
        self.CP2105_SUSPEND = machine.Pin(4,machine.Pin.IN)
        
        self.CP2105_GPIO1.value(0)
        self.CP2105_GPIO0.value(0)
        self.CP2105_DCD_ECI.value(0)
        
    def send_message(self,message):
        self.uart0.write(message)
        time.sleep_ms(100)
        print(message)
    def read_message(self,buf):
        if(self.uart0.any()):
            self.uart0.readinto(buf)
            return True
        return False
#cp2105 = CP2105(time,machine,UART,Pin)    
#while True:
#    cp2105.send_message("test")
#    print("send")
#    time.sleep_ms(100)
#    if(cp2105.read_message(res_message)):
#        print(str(res_message.decode('utf-8')))
#        cp2105.send_message("Get" + str(res_message.decode('utf-8')))
#        time.sleep_ms(1000)
#        cp2105.send_message("K" + '\r\n')
#        res_message= bytearray(20)

