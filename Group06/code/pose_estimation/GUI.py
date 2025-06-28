from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtWidgets import QApplication

from MainWindow import Ui_MainWindow
import sys
import UseCamera.RaiseHand.testRH as RH
import UseCamera.deepSquat.testDS as DS

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(lambda: self.on_click1(1))
        self.pushButton_2.clicked.connect(lambda: self.on_click1(2))
        self.pushButton_3.clicked.connect(lambda: self.on_click1(3))

    def on_click1(self, id):
        # 根据按钮 ID 调用不同的函数或类方法
        if id == 1:
            RH.main()
        elif id == 2:
            DS.main()
        elif id == 3:
            QMessageBox.information(self, '消息', '该功能未更新')

        # 弹出消息框
        #QMessageBox.information(self, '消息', f'你点击了按钮 {id}')

# 运行程序
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())