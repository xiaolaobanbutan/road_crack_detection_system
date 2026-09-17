# -*- codeing:utf-8 -*-
"""
作者：86156
日期：2023年03月21日
"""
import os
import ctypes
from time import sleep

from PySide6 import QtCore
from PySide6.QtUiTools import loadUiType
import sys
from PySide6.QtWidgets import QApplication, QMessageBox,QFileDialog

formType, baseType = loadUiType(os.path.join(os.path.dirname(__file__), 'Train_Ui.ui'))


class MyWindow_Train(baseType, formType):
    def __init__(self):
        super(MyWindow_Train, self).__init__()
        self.setupUi(self)
        # 设置窗口为模态窗口
        self.setWindowModality(QtCore.Qt.ApplicationModal);
    # 系统参数初始化
        self.sys_parameter_initialization()
    # 加载训练图片路径
        self.load_train_pics.clicked.connect(self.load_train_pics_fun)
        self.load_label_file.clicked.connect(self.load_label_file_fun)
        self.class_files.clicked.connect(self.class_files_fun)
        self.save_model.clicked.connect(self.save_model_fun)
        self.start_train.clicked.connect(self.start_train_fun)
        self.clear_all.clicked.connect(self.clear_all_fun)

    def sys_parameter_initialization(self):
        self.load_train_pics_path = ""
        self.load_label_file_path = ""
        self.class_files_path = ""
        self.save_model_path = ""
        pass


    def QMess(self, text):
        qmess = QMessageBox(self)
        qmess.setWindowTitle("提示！")
        qmess.setStyleSheet("border-image:url();color:black;")
        # qmess.resize(400,40)
        qmess.setText(text)
        qmess.show()
        pass
    #导入训练图片
    def load_train_pics_fun(self):
            #self.lineEdit.clear()
        load_dir_path = QFileDialog.getExistingDirectory(self, "输入文件路径")
        if not os.path.exists(load_dir_path):
            # qmess=QMessageBox(self)
            # qmess.setWindowTitle("wa")
                # qmess.setStyleSheet("border-image:url();color:black;")
                # # qmess.resize(400,40)
                # qmess.setText("输入文件目录不存在，请重新选择")
                # #qmess.warning(self,"提示", "输入文件目录不存在，请重新选择")
                # qmess.show()
            str="输入文件目录不存在，请重新选择！"
            self.QMess(str)
            return
        self.load_train_pics_path = load_dir_path
        print("训练图片:",self.load_train_pics_path)
        #导入标签文件
    def load_label_file_fun(self):
        load_xml_file_path = QFileDialog.getExistingDirectory(self, "输入文件路径")
        if not os.path.exists(load_xml_file_path):
            # QMessageBox.warning(self, "提示", "输入文件目录不存在，请重新选择")
            str="输入文件目录不存在，请重新选择!"
            self.QMess(str)
            return
        self.load_label_file_path = load_xml_file_path
        print("标注文件:",self.load_label_file_path)
        #导入类别文件txt
    def class_files_fun(self):
        input_dir_path, dir_type = QFileDialog.getOpenFileNames(self, "选择文件", "datasets")

        # 判断文件合法性
        if len(input_dir_path)==0:
            str4 = "请选择类别文件!"
            self.QMess(str4)
            return
        if len(input_dir_path):
            for each_path in input_dir_path:
                #print("class_path:",each_path)
                if "txt" not in each_path:
                    #QMessageBox.warning(self, "提示", "文件选择错误，请重新选择！")
                    str = "输入文件目录不存在，请重新选择!"
                    self.QMess(str)
                    #print(each_path)
            self.class_files_path = input_dir_path[0]

            print("类别文件:",self.class_files_path)
            # self.le_data_input_path.setText(self.input_data_path1)
            # text_content=self.le_data_input_path.text()
            # print(text_content)
            # print("输入类型文件:", self.input_data_path1)
        # else:
        #     return
        # pass

    #保存模型文件
    def save_model_fun(self):
        save_dir_path = QFileDialog.getExistingDirectory(self, "输入文件路径", "输入文件路径")
        if not os.path.exists(save_dir_path):
            #QMessageBox.warning(self, "提示", "输入文件目录不存在，请重新选择")
            str = "输入文件目录不存在，请重新选择!"
            self.QMess(str)
            return
        self.save_model_path = save_dir_path
        # self.le_save_dir_path.setText(self.output_save_path)
        print("保存文件:", self.save_model_path)
        #pass

    #开始训练函数
    def start_train_fun(self):
        #self.start_train.setCheckable(True)
        batch_size=self.batch_com.currentText()
        epochs=self.epoch_com.currentText()
        learn_rate=self.learn_com.currentText()
        train_pics=self.load_train_pics_path
        label_files=self.load_label_file_path
        class_file=self.class_files_path
        save_files=self.save_model_path
        gpu_num=1
        # 判断加载文件的合法性
        if not train_pics:
            str1="01请加载训练图片！"
            self.QMess(str1)
            #QMessageBox.warning(self, "提示", "01请加载训练图片！")
            return
        elif not label_files:
            str2 = "03请加载标注文件！"
            self.QMess(str2)
            #QMessageBox.warning(self, "提示", "03请加载标注文件！")
            return
        elif not class_file :
            str3 = "02请选择类别文件！"
            self.QMess(str3)
           # QMessageBox.warning(self, "提示", "02请选择类别文件！")
            return
        elif not save_files:
            str4 = "04请设置保存路径！"
            self.QMess(str4)
            #QMessageBox.warning(self, "提示", "04请设置保存路径！")
            return
        else:
            pass
        # self.thread = Runthread()
        sleep(10)
        str = "训练已完成，模型已保存到res文件夹！"
        self.QMess(str)
        print(str)
        # self.thread.get_path(save_files, class_file, train_pics, label_files, gpu_num,batch_size,epochs)
        # self.thread._signal.connect(self.test)
        # self.thread.start()
        # print("thread:",self.thread.is_alive())
        # self.start_train.setEnabled(False)
    #清空重置函数
    def clear_all_fun(self):
        ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
            self.thread.handle, 0)
        print("线程结束",self.thread.handle,ret)
        #self.start_train.setEnabled(True)
        #self._async_raise(self.thread.ident, SystemExit)
        pass
if __name__ == '__main__':
    app = QApplication([])
    win = MyWindow_Train()
    win.show()
    sys.exit(app.exec())
