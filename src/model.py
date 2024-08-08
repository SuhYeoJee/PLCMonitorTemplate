if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCMonitorTemplate")
# -------------------------------------------------------------------------------------------
from configparser import ConfigParser
from random import randint
import json
# ===========================================================================================

# class connect_wait():
#     def __init__(self):
#         self.dataset = "CW"
#         self.check = ""
# class start_wait():...
# class exit_wait():...

# ===========================================================================================

class test_plc():
    def __init__(self):
        ...

    def _get_plc_word(self,addr:str,size:int=1)->str:
        return addr + '_' + str(randint(0,10)) + '_' + str(size)
    
    def _get_plc_bit(self,addr:str,size:int=1)->str:
        return addr + '_b' + (str(randint(0,1)) * size)
    
    def get_plc_data(self,addr:str)->str:
        addr,_,option = addr.partition('#')
        size = int(''.join(filter(str.isdigit, option)) or 1)
        if 'B' in option:
            return self._get_plc_bit(addr,size)
        else:
            return self._get_plc_word(addr,size)
    
    def get_plc_dataset(self,dataset:dict)->dict:
        return {k:self.get_plc_data(v) for k,v in dataset.items()}
        
# ===========================================================================================
class Model():
    def __init__(self):
        self.config = self.get_config()
        self.addrs = self.get_plc_addrs()
        self.plc = test_plc()
        # self.c_w, self.s_w, self.e_w = connect_wait(), start_wait(), exit_wait()
        # self.state = self.c_w

    # [PLC] -------------------------------------------------------------------------------------------


    # [json] -------------------------------------------------------------------------------------------
    def get_plc_addrs(self):
        with open("./src/spec/PLC_ADDR.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data 

    # [config] -------------------------------------------------------------------------------------------
    def get_config_item(self,item:str="text"):
        return self.config.get(item,"val")
    
    def get_config(self,section:str="DEFAULT",config_path:str="config.txt",enc:str="utf-8"):
        config = ConfigParser()
        config.read(config_path,enc)
        return config[section]
# ===========================================================================================
if __name__ == "__main__":
    m = Model()
    print(m.get_config_item('t'))
    print(m.addrs["PLC_ADDR"]["AUTOMATIC"]["PRGNO"])
    print(m.plc.get_plc_data('DW100'))
    print(m.plc.get_plc_data('DW100#21'))
    print(m.plc.get_plc_data('DW100#B21'))
