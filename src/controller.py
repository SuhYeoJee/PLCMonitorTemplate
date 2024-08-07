if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCMonitorTemplate")
# -------------------------------------------------------------------------------------------
from src.model import Model
from src.view import View    
from src.module.pyqt_imports import *
from src.module.exceptions import *
# ===========================================================================================
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        # [btn mapping] --------------------------
        self.view.pushButton.clicked.connect(self.set_lineEdit_plc_data)

    # -------------------------------------------------------------------------------------------
    def set_lineEdit_plc_data(self):
        from random import randint
        
        plc_data = self.model.get_plc_data("DW5004"+str(randint(1,10)))
        self.view.lineEdit.setText(plc_data)
        ...

# ===========================================================================================

def main():
    app = QApplication([])
    ctrl = Controller()
    ctrl.view.show()
    app.exec_()

if __name__ == "__main__":
    main()