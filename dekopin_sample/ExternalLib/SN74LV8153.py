#SN74LV8153.py

class SN74LV8153():
    # PIN No
    A_Y_0 = 0
    A_Y_1 = 1
    A_Y_2 = 2
    A_Y_3 = 3
    A_Y_4 = 4
    A_Y_5 = 5
    A_Y_6 = 6
    A_Y_7 = 7

    Y_0 = 0
    Y_1 = 1
    Y_2 = 2
    Y_3 = 3
    Y_4 = 4

    # LED No
    LED_A = A_Y_0
    LED_B = A_Y_1
    LED_C = A_Y_2
    LED_D = A_Y_3
    LED_E = A_Y_4
    LED_F = A_Y_5
    LED_G = A_Y_6
    LED_DP = A_Y_7
    LED_D1 = LED_A
    LED_D2 = LED_B
    LED_D3 = LED_C
    
    DIG_1 = Y_0
    DIG_2 = Y_1
    DIG_3 = Y_2
    DIG_4 = Y_3
    DIG_DP = Y_4
    def build_munber(self,number,digit):
        number_data = 0x00
        if(number ==-1):
            number_data = number_data + (0x01 << SN74LV8153.LED_G)
        if (number ==0):
            number_data = number_data + (0x01 << SN74LV8153.LED_A)
            number_data = number_data + (0x01 << SN74LV8153.LED_B)
            number_data = number_data + (0x01 << SN74LV8153.LED_C)    
            number_data = number_data + (0x01 << SN74LV8153.LED_D)
            number_data = number_data + (0x01 << SN74LV8153.LED_E)
            number_data = number_data + (0x01 << SN74LV8153.LED_F)
        elif(number ==1):
            number_data = number_data + (0x01 << SN74LV8153.LED_B)
            number_data = number_data + (0x01 << SN74LV8153.LED_C)
        elif(number ==2):
            number_data = number_data + (0x01 << SN74LV8153.LED_A)
            number_data = number_data + (0x01 << SN74LV8153.LED_B)
            number_data = number_data + (0x01 << SN74LV8153.LED_D)
            number_data = number_data + (0x01 << SN74LV8153.LED_E)
            number_data = number_data + (0x01 << SN74LV8153.LED_G)
        elif(number ==3):
            number_data = number_data + (0x01 << SN74LV8153.LED_A)
            number_data = number_data + (0x01 << SN74LV8153.LED_B)
            number_data = number_data + (0x01 << SN74LV8153.LED_C)
            number_data = number_data + (0x01 << SN74LV8153.LED_D)
            number_data = number_data + (0x01 << SN74LV8153.LED_G)
        elif(number ==4):
            number_data = number_data + (0x01 << SN74LV8153.LED_B)
            number_data = number_data + (0x01 << SN74LV8153.LED_C)
            number_data = number_data + (0x01 << SN74LV8153.LED_F)
            number_data = number_data + (0x01 << SN74LV8153.LED_G)
        elif(number ==5):
            number_data = number_data + (0x01 << SN74LV8153.LED_A)
            number_data = number_data + (0x01 << SN74LV8153.LED_C)
            number_data = number_data + (0x01 << SN74LV8153.LED_D)
            number_data = number_data + (0x01 << SN74LV8153.LED_F)
            number_data = number_data + (0x01 << SN74LV8153.LED_G)
        elif(number ==6):
            number_data = number_data + (0x01 << SN74LV8153.LED_A)
            number_data = number_data + (0x01 << SN74LV8153.LED_C)
            number_data = number_data + (0x01 << SN74LV8153.LED_D)
            number_data = number_data + (0x01 << SN74LV8153.LED_E)
            number_data = number_data + (0x01 << SN74LV8153.LED_F)
            number_data = number_data + (0x01 << SN74LV8153.LED_G)
        elif(number ==7):
            number_data = number_data + (0x01 << SN74LV8153.LED_A)
            number_data = number_data + (0x01 << SN74LV8153.LED_B)
            number_data = number_data + (0x01 << SN74LV8153.LED_C)
        elif(number ==8):
            number_data = number_data + (0x01 << SN74LV8153.LED_A)
            number_data = number_data + (0x01 << SN74LV8153.LED_B)
            number_data = number_data + (0x01 << SN74LV8153.LED_C)
            number_data = number_data + (0x01 << SN74LV8153.LED_D)
            number_data = number_data + (0x01 << SN74LV8153.LED_E)
            number_data = number_data + (0x01 << SN74LV8153.LED_F)
            number_data = number_data + (0x01 << SN74LV8153.LED_G)
        elif(number ==9):
            number_data = number_data + (0x01 << SN74LV8153.LED_A)
            number_data = number_data + (0x01 << SN74LV8153.LED_B)
            number_data = number_data + (0x01 << SN74LV8153.LED_C)
            number_data = number_data + (0x01 << SN74LV8153.LED_D)
            number_data = number_data + (0x01 << SN74LV8153.LED_F)
            number_data = number_data + (0x01 << SN74LV8153.LED_G)
        self.number_data[0] = number_data
        digit_data = 0x00
        if (digit ==0):
            digit_data = digit_data + (0x01 << SN74LV8153.DIG_4)
        elif(digit ==1):
            digit_data = digit_data + (0x01 << SN74LV8153.DIG_3)
        elif(digit ==2):
            digit_data = digit_data + (0x01 << SN74LV8153.DIG_2)
        elif(digit ==3):
            digit_data = digit_data + (0x01 << SN74LV8153.DIG_1)
        self.digit_data[0] = digit_data
        
    def __init__(self,machine,UART,Pin,time,_thread):
        self.machine = machine
        self.time = time
        self._thread = _thread
        self.uart0 = UART(0, baudrate=50000, tx=Pin(16), rx=Pin(1))
        self.SHIFT_REG_REEST = machine.Pin(12,machine.Pin.OUT)
        self.SHIFT_REG_REEST.value(1)
        self.SHIFT_REG_SOUT = machine.Pin(13,machine.Pin.IN)

#        print("start")
        self.counta = 1
        self.number_data = bytearray(1)
        self.digit_data = bytearray(1)
        self.shift_ref_data0 = bytearray(1)
        self.shift_ref_data1 = bytearray(1)
        self.counta_shift_reg = 0
        self.SHIFT_REG_REEST.value(0)
        self.time.sleep_ms(100)
        self.SHIFT_REG_REEST.value(1)
        self.lock = _thread.allocate_lock()
        self.is_continue = 1
        self.number = 0
        self.is_On = False
        self.is_Flashing = False
        self._thread.start_new_thread(self.LED_thread, ())
    def LED_thread(self):
        is_continue = 1
        number = 0
        is_On = False
        is_Flashing = False
        flashing_counta = 0
        while True:
            lockP = self.lock.acquire(1, -1)
            if lockP:
                number = self.number
                is_On = self.is_On
                is_Flashing = self.is_Flashing
                is_continue = self.is_continue
                self.lock.release()        
            if(is_continue == 0):
                self.clear_LED()
                break
            if is_Flashing:
                if(flashing_counta >= 200):
                    self.update_display(number,False)
                else:
                    self.update_display(number,is_On)
                if (flashing_counta >= 500):
                    flashing_counta = 0
            else:
                self.update_display(number,is_On)
            self.time.sleep_ms(1)
            flashing_counta += 1
                
    def update_display(self,number,is_On):
        is_minus = False
        if(number < 0):
            is_minus = True
        if(not is_On):
            self.clear_LED()
            return
        num_d1 = abs(number) % 10
        self.set_LED(num_d1,0)
        if(abs(number) < 10):
            if(is_minus):
                self.set_LED(-1,1)
            return
        num_d2 = (int(abs(number)/10)) % 10
        self.set_LED(num_d2,1)
        if(abs(number) < 100):
            if(is_minus):
                self.set_LED(-1,2)
            return
        num_d3 = (int(abs(number)/100)) % 10
        self.set_LED(num_d3,2)
        if(abs(number) < 1000):
            if(is_minus):
                self.set_LED(-1,3)
            return
        num_d4 = (int(abs(number)/1000)) % 10
        self.set_LED(num_d4,3)
        
    def clear_LED(self):
        self.shift_ref_data0[0] = 0b00000001
        self.shift_ref_data1[0] = 0b00000001
        self.uart0.write(self.shift_ref_data0)
        self.uart0.write(self.shift_ref_data1)
        self.shift_ref_data0[0] = 0b00000011 + 0b11110000
        self.shift_ref_data1[0] = 0b00000011 + 0b11110000
        self.uart0.write(self.shift_ref_data0)
        self.uart0.write(self.shift_ref_data1)
    def set_LED(self,number,digit):
        self.clear_LED()
        self.build_munber(number,digit)
        self.shift_ref_data0[0] = 0b00000001 + ((self.digit_data[0] & 0b1111) << 4)
        self.shift_ref_data1[0] = 0b00000001 + ((self.digit_data[0] & 0b11110000))
#        print("{}:{}:{}".format(self.counta_shift_reg,self.shift_ref_data0[0],self.shift_ref_data1[0]))  # write 5 bytes
        self.uart0.write(self.shift_ref_data0)
        self.uart0.write(self.shift_ref_data1)
        self.shift_ref_data0[0] = 0b00000011 + ((~self.number_data[0] & 0b1111) << 4)
        self.shift_ref_data1[0] = 0b00000011 + ((~self.number_data[0] & 0b11110000))
        self.uart0.write(self.shift_ref_data0)
        self.uart0.write(self.shift_ref_data1)
        self.time.sleep_ms(1)

#        print(":{}:{}".format(self.number_data[0],self.digit_data[0]))  # write 5 bytes
#        print(":{}:{}".format(self.shift_ref_data0[0],self.shift_ref_data1[0]))  # write 5 bytes
    def set_number(self,number,is_On,is_Flashing = False):
        lockP = self.lock.acquire(1, -1)
        if lockP:
            self.is_On = is_On
            self.number = number
            self.is_Flashing = is_Flashing
            self.lock.release()

    def set_stop(self):
        lockP = self.lock.acquire(1, -1)
        while True:
            if lockP:
                self.is_continue = 0
                self.lock.release()
                break
