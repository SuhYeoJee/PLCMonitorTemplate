if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCMonitorTemplate")
# -------------------------------------------------------------------------------------------
from configparser import ConfigParser
import json
# ===========================================================================================
class Model():
    def __init__(self):
        self.config = self.get_config()
        self.addrs = self.get_plc_addrs()

    # [PLC] -------------------------------------------------------------------------------------------
    def get_plc_data(self,addr:str,size:int=1):
        return addr
        ...

    def get_plc_dataset(self,dataset:str):
        ...

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
