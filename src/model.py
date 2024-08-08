if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCMonitorTemplate")
# -------------------------------------------------------------------------------------------
from configparser import ConfigParser
from random import randint
import json
# ===========================================================================================

class state_wait():
    def __init__(self):
        self.addrs = self.get_plc_addrs()
        self.dataset = None
        self.next_state = None
    # [json] -------------------------------------------------------------------------------------------
    def get_plc_addrs(self):
        with open("./src/spec/PLC_ADDR.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data 
    
    def _is_next(self,val)->bool:...

class test_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["TEST"]
        self.key = "PRGNO"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False

class connect_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["CONNECT"]
        self.key = "CONNECT"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False
class start_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["START"]
        self.key = "ON"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False
class exit_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["EXIT"]                
        self.key = "ON"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False
# ===========================================================================================

class test_plc():
    def __init__(self):
        ...

    def _get_plc_word(self,addr:str,size:int=1)->str:
        return addr + '_' + str(size)  + '_' + str(randint(0,1))
    
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
        self.plc = test_plc()
        self._init_state()

    def _init_state(self)->None:
        self.t_w = test_wait()
        self.c_w, self.s_w, self.e_w = connect_wait(), start_wait(), exit_wait()
        self.t_w.next_state = self.c_w
        self.c_w.next_state = self.s_w
        self.s_w.next_state = self.e_w
        self.e_w.next_state = self.s_w
        # --------------------------
        self.state = self.t_w

    # [PLC] -------------------------------------------------------------------------------------------
    def _get_update_data(self)->dict:
        return self.plc.get_plc_dataset(self.state.dataset)

    def _change_mode(self)->None:
        self.state = self.state.next_state

    def worker_tick(self)->dict:
        update_data = self._get_update_data() # plc 데이터 읽기
        print(update_data)
        is_next = self.state._is_next(update_data[self.state.key]) # 읽은 항목에서 state체크
        if is_next: # state 넘어가기
            self._change_mode()
        return update_data

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
    ## config test
    # print(m.get_config_item('t'))
    ## json test
    # print(m.state.addrs["PLC_ADDR"]["AUTOMATIC"]["PRGNO"])
    ## ADDR PASING
    # print(m.plc.get_plc_data('DW100'))
    # print(m.plc.get_plc_data('DW100#21'))
    ## worker tick test
    # for i in range(100):
    #     print(m.worker_tick())


