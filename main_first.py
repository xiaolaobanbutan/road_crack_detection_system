# -*- codeing:utf-8 -*-
"""
作者：86156
日期：2023年03月21日
"""
# from PySide6.QtWidgets import QApplication,QMainWindow
# from First_Ui import Ui_MainWindow
# import sys
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow,self).__init__()
#         self.ui=Ui_MainWindow()
#         self.ui.setupUi(self)


import os
from PySide6 import QtWidgets
from labelImg import MainWindow
from window_train_main import Train_window
from First_Ui import *
import sys
from lib.share import shareInfo # 公共变量名
from recognizition import MyWindow
# formType, baseType = loadUiType('First_Ui.ui')
sys.setrecursionlimit(1000000)

class Main_window(QtWidgets.QMainWindow, MyWindow_First):
    def __init__(self):
        super(Main_window, self).__init__()
        self.setupUi(self)

        argv = []
        self.child1 = MainWindow(argv[1] if len(argv) >= 2 else None,
                                 argv[2] if len(argv) >= 3 else os.path.join(
                                     os.path.dirname(sys.argv[0]),
                                     'data', 'predefined_classes.txt'),
                                 argv[3] if len(argv) >= 4 else None)
        # 设置窗口参数
        self.model_train.clicked.connect(self.model_train_fun)
        self.accurate_detecte.clicked.connect(self.accurate_detecte_fun)
        self.data_annno.clicked.connect(self.New)

    def model_train_fun(self):
        self.model_train.setEnabled(False)
        self.accurate_detecte.setEnabled(False)
        Train_Form = QtWidgets.QDialog()
        Train = Train_window()
        Train.setupUi(Train_Form)
        Train_Form.show()
        temp = Train_Form.exec()
        if temp == 0:
            Train_Form.close()
        self.Form.show()
        self.model_train.setEnabled(True)
        self.accurate_detecte.setEnabled(True)

    def accurate_detecte_fun(self):
        self.accurate_detecte.setEnabled(False)
        self.model_train.setEnabled(False)
        print("nihoa")
        shareInfo.createWin = MyWindow()
        shareInfo.createWin.show()
        self.accurate_detecte.setEnabled(True)
        self.model_train.setEnabled(True)
    # def data_annodate_fun(self):
    #     self.Form.close()
    #     argv = []
    #     app2 = QApplication(argv)
    #     win = MainWindow(argv[1] if len(argv) >= 2 else None,
    #                      argv[2] if len(argv) >= 3 else os.path.join(
    #                          os.path.dirname(sys.argv[0]),
    #                          'data', 'predefined_classes.txt'),
    #                      argv[3] if len(argv) >= 4 else None)
    #     win.show()
    #     win.exec_()
    #     pass
    def New(self):
        print("nihao")
        # self.gridLayout.addWidget(self.child1)
        self.child1.show()
        # shareInfo.createWin = MainWindow()
        # shareInfo.createWin.show()
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Main_window()
    win.show()
    sys.exit(app.exec())
