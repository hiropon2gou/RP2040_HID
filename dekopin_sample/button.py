#button.py 

import sys
class button():
    def __init__(self,machine,Pin,micropython,freq):
        self.freq = freq            
        self.micropython = micropython
        self.WS1 = machine.Pin(20,machine.Pin.IN,Pin.PULL_UP)
        self.WS2 = machine.Pin(21,machine.Pin.IN,Pin.PULL_UP)
        self.is_push_ws1_flag = False
        self.is_push_ws2_flag = False
        self.set_push_ws1_flag_ref = self.set_push_ws1_flag
        self.set_push_ws2_flag_ref = self.set_push_ws2_flag
        self.WS1.irq(trigger = Pin.IRQ_FALLING ,handler = self.ws1_irq)
        self.WS2.irq(trigger = Pin.IRQ_FALLING ,handler = self.ws2_irq)
        self.is_long_pushing_ws1 = False
        self.long_pushing_counta_ws1 = 0
        self.is_long_pushing_ws2 = False
        self.long_pushing_counta_ws2 = 0
#        if(self.WS1.value() == 0):
#            sys.exit()
    def update_button_state(self):
        if(self.WS1.value() == 0):
#            print("WS1")
            self.long_pushing_counta_ws1 += 1
        else:
            self.long_pushing_counta_ws1 = 0

        if(self.long_pushing_counta_ws1 >= self.freq * 3):
#            print("WS1")
            self.long_pushing_counta_ws1 = self.freq * 3
            self.is_long_pushing_ws1 = True
        else:
            self.is_long_pushing_ws1 = False

        if(self.WS2.value() == 0):
#            print("WS2")
            self.long_pushing_counta_ws2 += 1
        else:
            self.long_pushing_counta_ws2 = 0
            
        if(self.long_pushing_counta_ws2 >= self.freq * 3):
            self.long_pushing_counta_ws2 = self.freq * 3
            self.is_long_pushing_ws2 = True
        else:
            self.is_long_pushing_ws2 = False

    def get_ws1(self):
        return self.WS1.value()
    def get_ws2(self):
        return self.WS2.value()
    def set_push_ws1_flag(self,_):
        self.is_push_ws1_flag = True
    def set_push_ws2_flag(self,_):
        self.is_push_ws2_flag = True

    def ws1_irq(self,p):
        self.micropython.schedule(self.set_push_ws1_flag_ref, 0)

    def ws2_irq(self,p):
        self.micropython.schedule(self.set_push_ws2_flag_ref, 0)
