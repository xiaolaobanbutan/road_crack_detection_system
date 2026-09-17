# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Train_Ui.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
import ctypes
import os
from time import sleep
from Model.unet_model import UNet
from utils.dataset import ISBI_Loader
from torch import optim
import torch.nn as nn
import torch
from tqdm import tqdm
import matplotlib.pyplot as plt
import time

import numpy as np
from tqdm import tqdm

import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
# 忽略烦人的红色提示
import warnings
from torchvision import datasets
from torchvision import models
import torch.optim as optim
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget,QMessageBox, QFileDialog)
import app_rc
import apprcc_rc

class MyWindow_Train(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(882, 672)
        icon = QIcon()
        icon.addFile(u":/img/img/icons/swimming.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"border-image: url(:/img/Settings/main_window_img/background1x.png);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_7 = QSpacerItem(18, 28, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_7)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(22)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.horizontalLayout_7.addWidget(self.label)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_8 = QSpacerItem(18, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_10)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.load_train_pics = QPushButton(self.centralwidget)
        self.load_train_pics.setObjectName(u"load_train_pics")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_train_pics.sizePolicy().hasHeightForWidth())
        self.load_train_pics.setSizePolicy(sizePolicy)
        self.load_train_pics.setMinimumSize(QSize(231, 231))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.load_train_pics.setFont(font1)
        self.load_train_pics.setLayoutDirection(Qt.LeftToRight)
        self.load_train_pics.setStyleSheet(u"\n"
"QPushButton#load_train_pics{border-image: url(:/img/Settings/train_model_img/load_imgA.png);\n"
"border-radius: 15px;}\n"
"QPushButton#load_train_pics::hover{\n"
"border-image: url(:/img/Settings/train_model_img/load_imgB.png);\n"
"border-radius: 15px;\n"
"}")

        self.horizontalLayout.addWidget(self.load_train_pics)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.class_files = QPushButton(self.centralwidget)
        self.class_files.setObjectName(u"class_files")
        self.class_files.setMinimumSize(QSize(231, 231))
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.class_files.setFont(font2)
        self.class_files.setStyleSheet(u"QPushButton#class_files{border-image: url(:/img/Settings/train_model_img/label_txt_imgB.png);\n"
"border-radius: 15px;}\n"
"QPushButton#class_files::hover{\n"
"border-image: url(:/img/Settings/train_model_img/label_txt_imgA.png);\n"
"border-radius: 15px;\n"
"}")

        self.horizontalLayout.addWidget(self.class_files)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(18, 28, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.load_label_file = QPushButton(self.centralwidget)
        self.load_label_file.setObjectName(u"load_label_file")
        self.load_label_file.setMinimumSize(QSize(231, 231))
        self.load_label_file.setFont(font2)
        self.load_label_file.setStyleSheet(u"QPushButton#load_label_file{border-image: url(:/img/Settings/train_model_img/loa_annoB.png);\n"
"border-radius: 15px;}\n"
"QPushButton#load_label_file::hover{\n"
"border-image: url(:/img/Settings/train_model_img/loa_annoA.png);\n"
"border-radius: 15px;\n"
"}")

        self.horizontalLayout_2.addWidget(self.load_label_file)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.save_model = QPushButton(self.centralwidget)
        self.save_model.setObjectName(u"save_model")
        self.save_model.setMinimumSize(QSize(231, 231))
        self.save_model.setFont(font2)
        self.save_model.setStyleSheet(u"QPushButton#save_model{border-image: url(:/img/Settings/train_model_img/save_path_imgB.png);\n"
"border-radius: 15px;}\n"
"QPushButton#save_model::hover{\n"
"border-image: url(:/img/Settings/train_model_img/save_path_imgA.png);\n"
"border-radius: 15px;\n"
"}\n"
"")

        self.horizontalLayout_2.addWidget(self.save_model)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_8.addLayout(self.verticalLayout)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_9)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        font3 = QFont()
        font3.setFamilies([u"Arial"])
        font3.setBold(True)
        self.label_6.setFont(font3)
        self.label_6.setStyleSheet(u"color:rgba(173,180,170,1);\n"
"font-size:20px")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.clear_all = QPushButton(self.centralwidget)
        self.clear_all.setObjectName(u"clear_all")
        font4 = QFont()
        font4.setBold(True)
        self.clear_all.setFont(font4)
        self.clear_all.setStyleSheet(u"color:rgba(173,180,170,1);\n"
"font-size:20px")

        self.horizontalLayout_6.addWidget(self.clear_all)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_5)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.trainmodel = QLabel(self.centralwidget)
        self.trainmodel.setObjectName(u"trainmodel")
        self.trainmodel.setStyleSheet(u"color:rgba(173,180,170,1);font-size:20px")

        self.horizontalLayout_10.addWidget(self.trainmodel)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(0, 30))
        self.comboBox.setStyleSheet(u"background-color:rgba(65,72,112,1);color:white;")

        self.horizontalLayout_10.addWidget(self.comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.batch_size = QLabel(self.centralwidget)
        self.batch_size.setObjectName(u"batch_size")
        self.batch_size.setMinimumSize(QSize(3, 0))
        font5 = QFont()
        font5.setFamilies([u"Arial"])
        self.batch_size.setFont(font5)
        self.batch_size.setStyleSheet(u"color:rgba(173,180,170,1);font-size:20px")

        self.horizontalLayout_3.addWidget(self.batch_size)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.batch_com = QComboBox(self.centralwidget)
        self.batch_com.addItem("")
        self.batch_com.addItem("")
        self.batch_com.addItem("")
        self.batch_com.addItem("")
        self.batch_com.addItem("")
        self.batch_com.addItem("")
        self.batch_com.setObjectName(u"batch_com")
        self.batch_com.setMinimumSize(QSize(80, 29))
        self.batch_com.setStyleSheet(u"background-color:rgba(65,72,112,1);color:white;")

        self.horizontalLayout_3.addWidget(self.batch_com)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.epochs = QLabel(self.centralwidget)
        self.epochs.setObjectName(u"epochs")
        self.epochs.setFont(font5)
        self.epochs.setStyleSheet(u"color:rgba(173,180,170,1);font-size:20px")

        self.horizontalLayout_4.addWidget(self.epochs)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.epoch_com = QComboBox(self.centralwidget)
        self.epoch_com.addItem("")
        self.epoch_com.addItem("")
        self.epoch_com.addItem("")
        self.epoch_com.addItem("")
        self.epoch_com.addItem("")
        self.epoch_com.addItem("")
        self.epoch_com.addItem("")
        self.epoch_com.setObjectName(u"epoch_com")
        self.epoch_com.setMinimumSize(QSize(80, 29))
        self.epoch_com.setStyleSheet(u"background-color:rgba(65,72,112,1);color:white;")

        self.horizontalLayout_4.addWidget(self.epoch_com)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.learn_rate = QLabel(self.centralwidget)
        self.learn_rate.setObjectName(u"learn_rate")
        self.learn_rate.setFont(font5)
        self.learn_rate.setStyleSheet(u"color:rgba(173,180,170,1);font-size:20px")

        self.horizontalLayout_5.addWidget(self.learn_rate)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.learn_com = QComboBox(self.centralwidget)
        self.learn_com.addItem("")
        self.learn_com.addItem("")
        self.learn_com.addItem("")
        self.learn_com.addItem("")
        self.learn_com.addItem("")
        self.learn_com.setObjectName(u"learn_com")
        self.learn_com.setMinimumSize(QSize(100, 29))
        self.learn_com.setStyleSheet(u"background-color:rgba(65,72,112,1);color:white;")

        self.horizontalLayout_5.addWidget(self.learn_com)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_6)

        self.start_train = QPushButton(self.centralwidget)
        self.start_train.setObjectName(u"start_train")
        self.start_train.setMinimumSize(QSize(231, 231))
        self.start_train.setFont(font2)
        self.start_train.setStyleSheet(u"QPushButton#start_train{border-image: url(:/img/Settings/train_model_img/start_train.PNG);\n"
"border-radius: 15px;}")

        self.verticalLayout_3.addWidget(self.start_train)


        self.horizontalLayout_8.addLayout(self.verticalLayout_3)


        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_11)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.verticalSpacer_9 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_9)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        # MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        # QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u8bad\u7ec3\u754c\u9762", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8bad \u7ec3 \u6a21 \u578b", None))
        self.load_train_pics.setText("")
        self.class_files.setText("")
        self.load_label_file.setText("")
        self.save_model.setText("")
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u53c2\u6570\u8bbe\u7f6e", None))
        self.clear_all.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a\u91cd\u7f6e", None))
        self.trainmodel.setText(QCoreApplication.translate("MainWindow", u"\u8bad\u7ec3\u6a21\u578b\u79cd\u7c7b", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u88c2\u7f1d\u5206\u7c7b", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u88c2\u7f1d\u5206\u5272", None))

        self.batch_size.setText(QCoreApplication.translate("MainWindow", u"batch_size", None))
        self.batch_com.setItemText(0, QCoreApplication.translate("MainWindow", u"2", None))
        self.batch_com.setItemText(1, QCoreApplication.translate("MainWindow", u"4", None))
        self.batch_com.setItemText(2, QCoreApplication.translate("MainWindow", u"8", None))
        self.batch_com.setItemText(3, QCoreApplication.translate("MainWindow", u"16", None))
        self.batch_com.setItemText(4, QCoreApplication.translate("MainWindow", u"32", None))
        self.batch_com.setItemText(5, QCoreApplication.translate("MainWindow", u"64", None))

        self.epochs.setText(QCoreApplication.translate("MainWindow", u"epochs", None))
        self.epoch_com.setItemText(0, QCoreApplication.translate("MainWindow", u"50", None))
        self.epoch_com.setItemText(1, QCoreApplication.translate("MainWindow", u"100", None))
        self.epoch_com.setItemText(2, QCoreApplication.translate("MainWindow", u"200", None))
        self.epoch_com.setItemText(3, QCoreApplication.translate("MainWindow", u"300", None))
        self.epoch_com.setItemText(4, QCoreApplication.translate("MainWindow", u"400", None))
        self.epoch_com.setItemText(5, QCoreApplication.translate("MainWindow", u"600", None))
        self.epoch_com.setItemText(6, QCoreApplication.translate("MainWindow", u"1000", None))

        self.learn_rate.setText(QCoreApplication.translate("MainWindow", u"learning_rate", None))
        self.learn_com.setItemText(0, QCoreApplication.translate("MainWindow", u"0.00001", None))
        self.learn_com.setItemText(1, QCoreApplication.translate("MainWindow", u"0.0001", None))
        self.learn_com.setItemText(2, QCoreApplication.translate("MainWindow", u"0.001", None))
        self.learn_com.setItemText(3, QCoreApplication.translate("MainWindow", u"0.01", None))
        self.learn_com.setItemText(4, QCoreApplication.translate("MainWindow", u"0.1", None))

        self.start_train.setText("")
        # 系统参数初始化
        self.sys_parameter_initialization()
        # 加载训练图片路径
        self.load_train_pics.clicked.connect(self.load_train_pics_fun)
        self.load_label_file.clicked.connect(self.load_label_file_fun)
        self.class_files.clicked.connect(self.class_files_fun)
        self.save_model.clicked.connect(self.save_model_fun)
        self.start_train.clicked.connect(self.start_train_fun)
    # retranslateUi
    def sys_parameter_initialization(self):
        self.load_train_pics_path=""
        self.load_label_file_path=""
        self.class_files_path=""
        self.save_model_path=""
        pass

    def QMess(self,text):
        qmess = QMessageBox(self)
        qmess.setWindowTitle("提示！")
        qmess.setStyleSheet("border-image:url();color:black;")
        # qmess.resize(400,40)
        qmess.setText(text)
        qmess.show()
        pass

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

    def load_label_file_fun(self):
        load_xml_file_path = QFileDialog.getExistingDirectory(self, "输入文件路径")
        if not os.path.exists(load_xml_file_path):
            # QMessageBox.warning(self, "提示", "输入文件目录不存在，请重新选择")
            str="输入文件目录不存在，请重新选择!"
            self.QMess(str)
            return
        self.load_label_file_path = load_xml_file_path
        print("标注文件:",self.load_label_file_path)
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

    def start_train_fun(self):
        #self.start_train.setCheckable(True)
        # 训练准备文件
        def train_net(net, device, data_path, epochs=40, batch_size=1, lr=0.00001):
            # 加载训练集
            isbi_dataset = ISBI_Loader(data_path)
            per_epoch_num = len(isbi_dataset) / batch_size
            train_loader = torch.utils.data.DataLoader(dataset=isbi_dataset,
                                                       batch_size=batch_size,
                                                       shuffle=True)
            # 定义RMSprop算法
            optimizer = optim.RMSprop(net.parameters(), lr=lr, weight_decay=1e-8, momentum=0.9)
            # 定义Loss算法
            criterion = nn.BCEWithLogitsLoss()
            # best_loss统计，初始化为正无穷
            best_loss = float('inf')
            # 训练epochs次
            with tqdm(total=epochs * per_epoch_num) as pbar:
                for epoch in range(epochs):
                    # 训练模式
                    net.train()
                    # 按照batch_size开始训练
                    for image, label in train_loader:
                        optimizer.zero_grad()
                        # 将数据拷贝到device中
                        image = image.to(device=device, dtype=torch.float32)
                        label = label.to(device=device, dtype=torch.float32)
                        # 使用网络参数，输出预测结果
                        pred = net(image)
                        # 计算loss
                        loss = criterion(pred, label)
                        # print('{}/{}：Loss/train'.format(epoch + 1, epochs), loss.item())
                        # 保存loss值最小的网络参数
                        if loss < best_loss:
                            best_loss = loss
                            torch.save(net.state_dict(), 'best_model_net.pth')
                        # 更新参数
                        loss.backward()
                        optimizer.step()
                        pbar.update(1)
        def train_class(dataset_dir,EPOCHS = 90,BATCH_SIZE = 4):
            warnings.filterwarnings("ignore")
            # windows操作系统
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
            plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
            # 有 GPU 就用 GPU，没有就用 CPU
            device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
            print('device', device)
            # 图像预处理
            # 训练集图像预处理：缩放裁剪、图像增强、转 Tensor、归一化
            train_transform = transforms.Compose([transforms.RandomResizedCrop(224),
                                                  transforms.RandomHorizontalFlip(),
                                                  transforms.ToTensor(),
                                                  transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                                                  ])
            # 测试集图像预处理-RCTN：缩放、裁剪、转 Tensor、归一化
            test_transform = transforms.Compose([transforms.Resize(256),
                                                 transforms.CenterCrop(224),
                                                 transforms.ToTensor(),
                                                 transforms.Normalize(
                                                     mean=[0.485, 0.456, 0.406],
                                                     std=[0.229, 0.224, 0.225])
                                                 ])
            # 载入图像分类数据集
            # 数据集文件夹路径
            # dataset_dir = 'data-crack_split'
            train_path = os.path.join(dataset_dir, 'train')
            test_path = os.path.join(dataset_dir, 'val')


            # 载入训练集
            train_dataset = datasets.ImageFolder(train_path, train_transform)

            # 载入测试集
            test_dataset = datasets.ImageFolder(test_path, test_transform)

            # 各类别名称
            class_names = train_dataset.classes
            n_class = len(class_names)
            # 映射关系：类别 到 索引号
            # train_dataset.class_to_idx
            # 映射关系：索引号 到 类别
            idx_to_labels = {y: x for x, y in train_dataset.class_to_idx.items()}
            # 保存为本地的 npy 文件
            np.save('labels.npy', idx_to_labels)
            np.save('idx.npy', train_dataset.class_to_idx)
            # 定义数据加载器DataLoader
            from torch.utils.data import DataLoader
            # 训练集的数据加载器
            train_loader = DataLoader(train_dataset,
                                      batch_size=BATCH_SIZE,
                                      shuffle=True,
                                      num_workers=0
                                      )

            # 测试集的数据加载器
            test_loader = DataLoader(test_dataset,
                                     batch_size=BATCH_SIZE,
                                     shuffle=False,
                                     num_workers=0
                                     )

            # # 微调训练所有层
            model = models.resnet18(pretrained=True)  # 载入预训练模型
            model.fc = nn.Linear(model.fc.in_features, n_class)
            optimizer = optim.Adam(model.parameters())
            # 训练配置
            model = model.to(device)
            # 交叉熵损失函数
            criterion = nn.CrossEntropyLoss()
            # 训练轮次 Epoch
            # 运行完整训练
            # 遍历每个 EPOCH
            for epoch in tqdm(range(EPOCHS)):
                model.train()
                for images, labels in train_loader:  # 获取训练集的一个 batch，包含数据和标注
                    images = images.to(device)
                    labels = labels.to(device)

                    outputs = model(images)  # 前向预测，获得当前 batch 的预测结果
                    loss = criterion(outputs, labels)  # 比较预测结果和标注，计算当前 batch 的交叉熵损失函数

                    optimizer.zero_grad()
                    loss.backward()  # 损失函数对神经网络权重反向传播求梯度
                    optimizer.step()  # 优化更新神经网络权重
            # 在测试集上初步测试
            model.eval()
            with torch.no_grad():
                correct = 0
                total = 0
                for images, labels in tqdm(test_loader):  # 获取测试集的一个 batch，包含数据和标注
                    images = images.to(device)
                    labels = labels.to(device)
                    outputs = model(images)  # 前向预测，获得当前 batch 的预测置信度
                    _, preds = torch.max(outputs, 1)  # 获得最大置信度对应的类别，作为预测结果
                    total += labels.size(0)
                    correct += (preds == labels).sum()  # 预测正确样本个数

                print('测试集上的准确率为 {:.3f} %'.format(100 * correct / total))
            torch.save(model, 'crack6_class.pth')

        clss=self.comboBox.currentText()

        bs=int(self.batch_com.currentText())
        print(bs)
        ep=int(self.epoch_com.currentText())
        print(ep)
        learn_rate=float(self.learn_com.currentText())
        print(learn_rate)
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
            # 选择设备，有cuda用cuda，没有就用cpu
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            # 加载网络，图片单通道1，分类为1。
            net = UNet(n_channels=1, n_classes=1)  # todo edit input_channels n_classes
            # 将网络拷贝到deivce中
            net.to(device=device)
            # 指定训练集地址，开始训练
            data_path = train_pics  # todo 修改为你本地的数据集位置
            print("进度条出现卡着不动不是程序问题，是他正在计算，请耐心等待")
            if clss=="裂缝分割":
                train_net(net, device, data_path, epochs=ep, batch_size=bs,lr=learn_rate)
            else:
                train_class(data_path,EPOCHS=ep,BATCH_SIZE = bs)
        # self.thread = Runthread()
        # self.thread.get_path(save_files, class_file, train_pics, label_files, gpu_num,batch_size,epochs)
        # self.thread._signal.connect(self.test)
        # self.thread.start()
        # sleep(10)
            str5="模型训练完成，已保存到{}文件".format(save_files)
            self.QMess(str5)
        # print("thread:",self.thread.is_alive())
        # self.start_train.setEnabled(False)

    def clear_all_fun(self):
        ret = ctypes.windll.kernel32.TerminateThread(  # @UndefinedVariable
            self.thread.handle, 0)
        print("线程结束",self.thread.handle,ret)
        #self.start_train.setEnabled(True)
        #self._async_raise(self.thread.ident, SystemExit)
        pass


