#Singleton.py
        
import json
import sys
import _thread
class Singleton:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @staticmethod 
    def getInstance():
        if Singleton.__instance == None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        if Singleton.__instance != None:
            pass
            # raise Exception("Singletonインスタンスがありません")
        else:
            Singleton.__instance = self        
        self.config_param = None
        self.time = None
        self.lock = _thread.allocate_lock()
        self.reboot_flag = False
        self.is_debug = False
    def is_debug(self,is_debug):
        self.is_debug = is_debug
    def set_lock(self,lock):
        self.lock = lock
    def set_time(self,time):
        self.time = time
    def set_config_param(self,config_param):
        self.config_param = config_param
    def save2flash(self):
        if self.is_debug:
            print("save2flash")
        self.time.sleep_ms(500)
        try:
            lockP = self.lock.acquire(1, 1.0)
            if lockP:
                json_str = json.dumps(self.config_param)
                json_str = json_str.replace(',', ',\r\n')
                json_str = json_str.replace('{', '{\r\n')
                json_str = json_str.replace('}', '\r\n}')
#                with open('Config/Parameter.json', encoding="utf-8", mode="w") as f:
#                    f.write(json_str)
                self.time.sleep_ms(100)
#                self.reboot_flag = True
                self.lock.release()
#            del lockP
            self.time.sleep_ms(100)
            if self.is_debug:
                print("saved")
        except Exception as e:
            print(e.value)       

    def load2flash(self):
        with open('Config/Parameter.json', encoding="utf-8", mode="r") as f:
            json_str = '' + f.read() + ''
            if self.is_debug:
                print(json_str)
            self.config_param = json.loads(json_str)
        self.time.sleep_ms(100)
