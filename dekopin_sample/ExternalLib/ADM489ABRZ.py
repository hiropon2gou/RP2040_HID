#ADM489ABRZ.py

class ADM489ABRZ():
    def __init__(self,time,machine,UART,Pin):
        self.time = time
        self.uart0 = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9))
        self.RS485_RE = machine.Pin(3,machine.Pin.OUT)
        self.RS485_DE = machine.Pin(2,machine.Pin.OUT)
        self.RS485_RE.value(0)
        self.RS485_DE.value(0)
    def send_message(self,message):
        self.RS485_DE.value(1)
        self.time.sleep_ms(10)
        self.uart0.write(message)
        self.time.sleep_ms(100)
        self.RS485_DE.value(0)
    def read_message(self,buf):
        if(self.uart0.any()):
            self.uart0.readinto(buf)
            return True
        return False
#while True:
#    send_message("test")
#    time.sleep_ms(100)
    

