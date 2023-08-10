#NAU7802.py

from machine import UART, Pin, I2C
import time
from Singleton import Singleton
#machine.freq(20000000)
class NAU7802_Cal_Status:
    NAU7802_CAL_SUCCESS = 0
    NAU7802_CAL_IN_PROGRESS = 1
    NAU7802_CAL_FAILURE = 2

class CTRL2_Bits:
    NAU7802_CTRL2_CALMOD = 0
    NAU7802_CTRL2_CALS = 2
    NAU7802_CTRL2_CAL_ERROR = 3
    NAU7802_CTRL2_CRS = 4
    NAU7802_CTRL2_CHS = 7

class Scale_Registers:
    NAU7802_PU_CTRL = 0x00
    NAU7802_CTRL1 = 0x01
    NAU7802_CTRL2 = 0x02
    NAU7802_OCAL1_B2 = 0x03
    NAU7802_OCAL1_B1 = 0x04
    NAU7802_OCAL1_B0 = 0x05
    NAU7802_GCAL1_B3 = 0x06
    NAU7802_GCAL1_B2 = 0x07
    NAU7802_GCAL1_B1 = 0x08
    NAU7802_GCAL1_B0 = 0x09
    NAU7802_OCAL2_B2 = 0x0A
    NAU7802_OCAL2_B1 = 0x0B
    NAU7802_OCAL2_B0 = 0x0C
    NAU7802_GCAL2_B3 = 0x0D
    NAU7802_GCAL2_B2 = 0x0E
    NAU7802_GCAL2_B1 = 0x01F
    NAU7802_GCAL2_B0 = 0x10
    NAU7802_I2C_CONTROL = 0x11
    NAU7802_ADCO_B2 = 0x12
    NAU7802_ADCO_B1 = 0x13
    NAU7802_ADCO_B0 = 0x14
    NAU7802_ADC = 0x15# //Shared ADC and OTP 32:24
    NAU7802_OTP_B1 = 0x15#     //OTP 23:16 or 7:0?
    NAU7802_OTP_B0 =0x16#      //OTP 15:8
    NAU7802_PGA = 0x1B
    NAU7802_PGA_PWR = 0x1C
    NAU7802_DEVICE_REV = 0x1F
class PGA_PWR_Bits:
    NAU7802_PGA_PWR_PGA_CURR = 0
    NAU7802_PGA_PWR_ADC_CURR = 2
    NAU7802_PGA_PWR_MSTR_BIAS_CURR = 4
    NAU7802_PGA_PWR_PGA_CAP_EN = 7

class PU_CTRL_Bits:
    NAU7802_PU_CTRL_RR = 0
    NAU7802_PU_CTRL_PUD = 1
    NAU7802_PU_CTRL_PUA = 2
    NAU7802_PU_CTRL_PUR = 3
    NAU7802_PU_CTRL_CS = 4
    NAU7802_PU_CTRL_CR = 5
    NAU7802_PU_CTRL_OSCS = 6
    NAU7802_PU_CTRL_AVDDS = 7
class NAU7802_SPS_Values:
    NAU7802_SPS_320 = 0b111
    NAU7802_SPS_80 = 0b011
    NAU7802_SPS_40 = 0b010
    NAU7802_SPS_20 = 0b001
    NAU7802_SPS_10 = 0b000
class NAU7802_Gain_Values:
    NAU7802_GAIN_128 = 0b111
    NAU7802_GAIN_64 = 0b110
    NAU7802_GAIN_32 = 0b101
    NAU7802_GAIN_16 = 0b100
    NAU7802_GAIN_8 = 0b011
    NAU7802_GAIN_4 = 0b010
    NAU7802_GAIN_2 = 0b001
    NAU7802_GAIN_1 = 0b000
class NAU7802_LDO_Values:
    NAU7802_LDO_2V4 = 0b111
    NAU7802_LDO_2V7 = 0b110
    NAU7802_LDO_3V0 = 0b101
    NAU7802_LDO_3V3 = 0b100
    NAU7802_LDO_3V6 = 0b011
    NAU7802_LDO_3V9 = 0b010
    NAU7802_LDO_4V2 = 0b001
    NAU7802_LDO_4V5 = 0b000

class NAU7802():
    def __init__(self,machine,I2C,Pin,time):
        self.singleton = Singleton.getInstance()
        self.is_debug = self.singleton.is_debug
        self.time = time
        self.i2c = I2C(1, freq=400000,sda= Pin(26), scl=Pin(27))          # ポートに依存して 400kHz の周波数でI2Cペリフェラルを
        self.addr = self.i2c.scan()                      # ペリフェラルをスキャンし、7ビットアドレスのリストを返します
        self.zero_data_list = list()
        self.calib_data_list = list()
        self.zero_data = self.singleton.config_param["loadcell"]["zero_bits"]
        self.old_zero_data = -100
        self.calib_data = self.singleton.config_param["loadcell"]["proof_waight_bits"]
        self.old_calib_data = -100

        self.waight = 1000 #1000gram
        if self.is_debug:
            print( "address is :" + str(self.addr) )
        self.address = 0x2A
        result = self.init()
        self.gram_list = list()
        self.peak_to_peak_data_limit = 50
        self.peak_to_peak_gram = 0
        self.peak_to_peak_gram_limit = 0.2
        self.gram = 1
        self.old_gram = -100
    # 作成します。使用するペリフェラルやピンを選択するために
    #laodcell_data = bytearray(3)      # バッファを作成
    def getRegister(self,register):
        self.time.sleep_us(1000)
        msg = bytearray(1)
        msg[0] = register
        ack = self.i2c.writeto(self.address,msg)         # 7ビットアドレス 42 のペリフェラルに３バイトを書き込みます
        if(ack == 0):
            return
        self.time.sleep_us(1000)        
        res = bytearray(1)
        self.i2c.readfrom_into(self.address,res)             # 7ビットアドレス 42 のペリフェラルから４バイトを読み込みます
        res_value = res[0]
        if self.is_debug:
            print("ack:{},add:{},register:{},getRegister_res:{}".format(ack,self.address,msg[0],res_value))
        return res_value
    def setRegister(self,registerAddress, value):
        self.time.sleep_us(1000)
        msg = bytearray(2)
        msg[0] = registerAddress
        msg[1] = value

        res = self.i2c.writeto(self.address,msg)         # 7ビットアドレス 42 のペリフェラルに３バイトを書き込みます
        if self.is_debug:
            print("res:{}".format(res))
        if (res == 0):
            return False#; //Sensor did not ACK
        return True

    def setBit(self,bitNumber, registerAddress):
        value = bytearray(1)
        value[0] = self.getRegister(registerAddress)
        value[0] = value[0] | (0x01 << bitNumber)# //Set this bit
        if self.is_debug:
            print("registerAddress:{},setBit:{}".format(registerAddress,value[0]))
        return (self.setRegister(registerAddress, value[0]))
    def getBit(self,bitNumber, registerAddress):
        value = bytearray(1)
        value[0] = self.getRegister(registerAddress)
        if self.is_debug:
            print("getBit:{},bitNumber:{}".format(value[0],bitNumber))
        res = value[0] & (0x01 << bitNumber)# //Clear all but this bit
        if(res >0):
            return True
        return False


    #Mask & clear a given bit within a register
    def clearBit(self,bitNumber, registerAddress):
        value = self.getRegister(registerAddress)
        value = value & ~(1 << bitNumber)# //Set this bit
        return (self.setRegister(registerAddress, value))

    def reset(self):
        self.setBit(PU_CTRL_Bits.NAU7802_PU_CTRL_RR, Scale_Registers.NAU7802_PU_CTRL)# //Set RR
        self.time.sleep_ms(1000)
        return (self.clearBit(PU_CTRL_Bits.NAU7802_PU_CTRL_RR, Scale_Registers.NAU7802_PU_CTRL))# //Clear RR to leave reset state

    def powerUp(self):
        self.setBit(PU_CTRL_Bits.NAU7802_PU_CTRL_PUD, Scale_Registers.NAU7802_PU_CTRL)
        self.setBit(PU_CTRL_Bits.NAU7802_PU_CTRL_PUA, Scale_Registers.NAU7802_PU_CTRL)

        #Wait for Power Up bit to be set - takes approximately 200us
        counter = 0
        while (1):
            res = self.getBit(PU_CTRL_Bits.NAU7802_PU_CTRL_PUR, Scale_Registers.NAU7802_PU_CTRL)
            if self.is_debug:
                print("counter:{},res:{}".format(counter,res))
            if (res == True):
                break# //Good to go
            self.time.sleep_ms(1)
            counter += 1 
            if (counter > 100):
                return False# //Error
        return True;
    def setLDO(self,ldoValue):
        if (ldoValue > 0b111):
            ldoValue = 0b111# //Error check

        #Set the value of the LDO
        value = self.getRegister(Scale_Registers.NAU7802_CTRL1)
        value = value & 0b11000111#    //Clear LDO bits
        value = value | ldoValue << 3# //Mask in new LDO bits
        self.setRegister(Scale_Registers.NAU7802_CTRL1, value)

        return (self.setBit(PU_CTRL_Bits.NAU7802_PU_CTRL_AVDDS, Scale_Registers.NAU7802_PU_CTRL))# //Enable the internal LDO

    def setGain(self,gainValue):
        if (gainValue > 0b111):
            gainValue = 0b111# //Error check

        value = self.getRegister(Scale_Registers.NAU7802_CTRL1)
        value = value & 0b11111000# //Clear gain bits
        value = value | gainValue#  //Mask in new bits

        return (self.setRegister(Scale_Registers.NAU7802_CTRL1, value))

    def setSampleRate(self,rate):
        if (rate > 0b111):
            rate = 0b111# //Error check

        value = self.getRegister(Scale_Registers.NAU7802_CTRL2)
        value = value & 0b10001111# //Clear CRS bits
        value = value | rate << 4#  //Mask in new CRS bits

        return (self.setRegister(Scale_Registers.NAU7802_CTRL2, value))
    def calAFEStatus(self):
        if (self.getBit(CTRL2_Bits.NAU7802_CTRL2_CALS, Scale_Registers.NAU7802_CTRL2)):
            return NAU7802_Cal_Status.NAU7802_CAL_IN_PROGRESS

        if (self.getBit(CTRL2_Bits.NAU7802_CTRL2_CAL_ERROR, Scale_Registers.NAU7802_CTRL2)):
            return NAU7802_Cal_Status.NAU7802_CAL_FAILURE

    #  // Calibration passed
        return NAU7802_Cal_Status.NAU7802_CAL_SUCCESS


    def waitForCalibrateAFE(self,timeout_ms):
        cal_ready = -1
        cal_ready = self.calAFEStatus()
        counta = 0
        while (cal_ready == NAU7802_Cal_Status.NAU7802_CAL_IN_PROGRESS):
            cal_ready = self.calAFEStatus()
            if counta > 10:
                break;
            self.time.sleep_us(1000)
            counta += 1
            if (cal_ready == NAU7802_Cal_Status.NAU7802_CAL_SUCCESS):
                return True
        if (cal_ready == NAU7802_Cal_Status.NAU7802_CAL_SUCCESS):
            return True

        return False

    def beginCalibrateAFE(self):
        self.setBit(CTRL2_Bits.NAU7802_CTRL2_CALS, Scale_Registers.NAU7802_CTRL2);
    def calibrateAFE(self):
        self.beginCalibrateAFE();
        return self.waitForCalibrateAFE(1000);

    def init(self):
        result = True
        result = result & self.reset() #Reset all registers
        if self.is_debug:
            print("reset" + str(result))
        result = result & self.powerUp()#Power on analog and digital sections of the scale
        if self.is_debug:
            print("powerUp" + str(result))
        result = result & self.setLDO(NAU7802_LDO_Values.NAU7802_LDO_2V4)#Set LDO to 3.3V NAU7802_LDO_2V4
#        result = result & self.setLDO(NAU7802_LDO_Values.NAU7802_LDO_3V3)#Set LDO to 3.3V NAU7802_LDO_2V4
        if self.is_debug:
            print("setLDO" + str(result))
        result = result & self.setGain(NAU7802_Gain_Values.NAU7802_GAIN_128)#Set gain to 128
        if self.is_debug:
            print("setGain" + str(result))
        result = result & self.setSampleRate(NAU7802_SPS_Values.NAU7802_SPS_80)#Set samples per second to 10
        if self.is_debug:
            print("setSampleRate" + str(result))
        result = result & self.setRegister(Scale_Registers.NAU7802_ADC, 0x30)#Turn off CLK_CHP. From 9.1 power on sequencing.
        if self.is_debug:
            print("setRegister" + str(result))
        result = result & self.setBit(PGA_PWR_Bits.NAU7802_PGA_PWR_PGA_CAP_EN, Scale_Registers.NAU7802_PGA_PWR)#Enable 330pF decoupling cap on chan 2. From 9.14 application circuit note.
        if self.is_debug:
            print("setBit" + str(result))
        result = result & self.calibrateAFE()#Re-cal analog front end when we change gain, sample rate, or channel
        if self.is_debug:
            print("calibrateAFE" + str(result))
        return result
    def get_average_gram(self):
        gram = float(self.get_data() - self.zero_data) * float(self.waight) / float(self.calib_data  - self.zero_data)
        self.gram_list.append(gram)
        max_gram = 0
        gram_sum_data = 0
        for gram_data in self.gram_list:
            if(max_gram < gram_data):
                max_gram = gram_data
            gram_sum_data += gram_data
        self.old_gram = self.gram 
        self.gram = float(gram_sum_data / len(self.gram_list))
        if(len(self.gram_list) > 20):
            del self.gram_list[0]
        self.peak_to_peak_gram = max_gram
        return self.gram

    def get_gram(self):
        self.gram = float(self.get_data() - self.zero_data) * float(self.waight) / float(self.calib_data  - self.zero_data)
        return self.gram       

    def get_data(self,count=3):
        average = 0.0
        for i in range(count):
            msg = bytearray(1)
            msg[0] = 0x12
            res = bytearray(3)
            laodcell_data = []
            ack = self.i2c.writeto(self.address, msg)
            if(ack == 0):
                return -1
            self.time.sleep_ms(10)        
            self.i2c.readfrom_into(self.address,res)             # 7ビットアドレス 42 のペリフェラルから４バイトを読み込みます
            data = res[0] << 16
            data = data + (res[1] << 8) #          //MidSB
            data = data + res[2] #              //LSB
#            print(str(data))  # write 5 bytes
            average += data
            
        return float(average/count)
