# -*- codeing:utf-8 -*-
"""
作者：86156
日期：2023年03月22日
"""
import sys
from PySide6 import QtWidgets
from PySide6.QtCore import QCoreApplication

from Train_Ui import MyWindow_Train
class Train_window(QtWidgets.QMainWindow,MyWindow_Train):
    def __init__(self):
        super(Train_window, self).__init__()
        self.setupUi(self)
        # 类函数实现

    def quit_fun(self):
        QCoreApplication.instance().quit()
        pass
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # Form = QtWidgets.QMainWindow()
    T = Train_window()
    # w.setupUi()
    # Form.show()
    T.show()
    sys.exit(app.exec())