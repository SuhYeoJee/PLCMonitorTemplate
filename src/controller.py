if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCMonitorTemplate")
# -------------------------------------------------------------------------------------------
from src.model import Model
from src.view import View    
from src.module.pyqt_imports import *
from src.module.exceptions import *
# ===========================================================================================
class Worker(QThread):
    data_generated = pyqtSignal()

    def __init__(self,time:int=5000):
        super().__init__()
        self.running = True
        self.time = time

    def run(self):
        while self.running:
            self.data_generated.emit() #self.time 주기로 함수 호출
            self.msleep(self.time)

    def stop(self):
        self.running = False
# ===========================================================================================
class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.worker = Worker()
        # [btn mapping] --------------------------
        self.view.pushButton.clicked.connect(self.exit_monitoring)
        # [update] --------------------------
        self.start_monitoring()

    # -------------------------------------------------------------------------------------------
    def set_lineEdit_plc_data(self):
        print('set_lineEdit_plc_data')
        plc_data = self.model.get_plc_data("DW5004")
        self.view.lineEdit.setText(plc_data)
    # --------------------------
    @pyqtSlot()
    def start_monitoring(self)->None:
        if not self.worker.isRunning():
            self.worker = Worker(1000)  # timer 주기적으로 show_now 호출
            self.worker.data_generated.connect(self.set_lineEdit_plc_data)  
            self.worker.start()   
    # --------------------------
    def exit_monitoring(self)->None:
        if self.worker.isRunning():
            self.worker.stop()

# ===========================================================================================

def main():
    app = QApplication([])
    ctrl = Controller()
    ctrl.view.show()
    app.exec_()

if __name__ == "__main__":
    main()