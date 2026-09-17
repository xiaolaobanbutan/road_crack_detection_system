import os
import shutil
import sys
import cv2
import numpy as np
from PySide6.QtGui import QPixmap, QImage, QMouseEvent, QGuiApplication,QAction
from PySide6.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QWidget, QApplication,QMenu
from PySide6.QtUiTools import QUiLoader, loadUiType
from PySide6.QtCore import QFile, QTimer, Qt, QEventLoop, QThread,QPoint
from PySide6 import QtCore, QtGui
from pathlib import Path
from utils.CustomMessageBox import MessageBox
from utils.capnums import Camera
from PIL import Image
from lib import glo
from YoloClass import YoloThread
from pytorchClass import PytorchThread
from crack_segclass import UnetThread
GLOBAL_STATE = True

formType, baseType = loadUiType(str(Path(__file__).resolve().parent / "ui" / "test_ui.ui"))


class YOLO(formType, baseType):
    def __init__(self):
        super().__init__()
        # 加载UI
        self.setupUi(self)
        self.setWindowFlags(Qt.CustomizeWindowHint)
        # ui部件功能设置
        self.inputPath = ""
        self.directory=""
        # Slider
        self.con_slider.valueChanged.connect(self.ValueChange)
        self.iou_slider.valueChanged.connect(self.ValueChange)
        self.latency_slider.valueChanged.connect(self.ValueChange)

        self.numcon = self.con_slider.value() / 100.0
        self.numiou = self.iou_slider.value() / 100.0
        self.numlatency = self.latency_slider.value()
        # 裂缝分割
        self.selpic.clicked.connect(self.open_pic)
        self.segpic.clicked.connect(self.seg_pic)
        self.selpics.clicked.connect(self.open_pics)
        self.segpics.clicked.connect(self.seg_pics)
        # 裂缝分类界面：
        self.file_single.clicked.connect(self.open_file)
        self.file_more.clicked.connect(self.open_files)
        self.file_video.clicked.connect(self.open_video)
        self.file_camera.clicked.connect(self.open_camera)
        # TOOLS
        self.folder.clicked.connect(self.Selectfile)
        self.importbtn.clicked.connect(self.Import)
        self.exporter.clicked.connect(self.Export)
        self.camera.clicked.connect(self.chose_cam)#摄像头
        # 最大化 最小化 关闭
        # 最大化按钮图片变化
        MaxIcon = QtGui.QIcon()
        MaxIcon.addPixmap(QtGui.QPixmap("./img/icons/square.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MaxIcon.addPixmap(QtGui.QPixmap("./img/icons/reduce.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        MaxIcon.addPixmap(QtGui.QPixmap("./img/icons/reduce.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.MaxButton.setCheckable(True)
        self.MaxButton.setIcon(MaxIcon)
        self.MaxButton.clicked.connect(self.max_or_restore)
        self.MinButton.clicked.connect(self.showMinimized)
        self.CloseButton.clicked.connect(self.close)
        # 视频预览
        self.input.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.output.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        # 视频操作
        # 播放按钮图片变化
        PlayIcon = QtGui.QIcon()
        PlayIcon.addPixmap(QtGui.QPixmap("./img/icons/play-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PlayIcon.addPixmap(QtGui.QPixmap("./img/icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        PlayIcon.addPixmap(QtGui.QPixmap("./img/icons/play-button.png"), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        PlayIcon.addPixmap(QtGui.QPixmap("./img/icons/pause.png"), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        PlayIcon.addPixmap(QtGui.QPixmap("./img/icons/play-button.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        PlayIcon.addPixmap(QtGui.QPixmap("./img/icons/pause.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        PlayIcon.addPixmap(QtGui.QPixmap("./img/icons/play-button.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        PlayIcon.addPixmap(QtGui.QPixmap("./img/icons/pause.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.playbtn.setCheckable(True)
        self.playbtn.setIcon(PlayIcon)
        self.det_btn.setCheckable(True)
        self.segpic.setCheckable(True)
        self.segpics.setCheckable(True)

        # 自动加载 pt文件
        self.comboBox.clear()
        self.pt_Path = "./ptmodel"
        self.pt_list = os.listdir('./ptmodel')
        self.pt_list = [file for file in self.pt_list if file.endswith('.pt')]
        self.pt_list.sort(key=lambda x: os.path.getsize('./ptmodel/' + x))
        self.comboBox.clear()
        self.comboBox.addItems(self.pt_list)
        self.qtimer_search = QTimer(self)
        self.qtimer_search.timeout.connect(lambda: self.search_pt())
        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(lambda: self.outputbox.clear())

        self.qtimer_search.start(2000)
        self.comboBox.currentTextChanged.connect(self.change_model)
        # 加载裂缝分裂pth文件
        self.select_model.clear()
        self.pth_Path = "./checkpoint"
        self.pth_list = os.listdir('./checkpoint')
        self.pth_list = [file for file in self.pth_list if file.endswith('.pth')]
        self.pth_list.sort(key=lambda x: os.path.getsize('./checkpoint/' + x))
        self.select_model.clear()
        self.select_model.addItems(self.pth_list)
        self.qthimer_search = QTimer(self)
        self.qthimer_search.timeout.connect(lambda: self.search_pth())
        self.qthimer = QTimer(self)
        self.qthimer.timeout.connect(lambda: self.output_text_path.clear())

        self.qthimer_search.start(2000)
        self.select_model.currentTextChanged.connect(self.change_pthmodel)
        # yolov7 thread
        self.yolo_thread = YoloThread()
        #pytorch thread
        self.torch_thread=PytorchThread()
        #Unet thread
        self.unet_thread=UnetThread()
        # 获取模型
        self.model_type = self.comboBox.currentText()
        self.yolo_thread.weights = "./ptmodel/%s" % self.model_type
        # 获取裂缝分裂模型
        self.pthmodel_type = self.select_model.currentText()
        self.torch_thread.weights = "./checkpoint/%s" % self.pthmodel_type

        self.yolo_thread.percent_length = self.progressBar.maximum()
        self.yolo_thread.send_input.connect(lambda x: self.showimg(x, self.input, 'img'))
        self.yolo_thread.send_output.connect(lambda x: self.showimg(x, self.output, 'img'))
        self.yolo_thread.send_result.connect(self.show_result)
        self.yolo_thread.send_msg.connect(lambda x: self.foot_print(x))
        self.yolo_thread.send_percent.connect(lambda x: self.progressBar.setValue(x))
        self.yolo_thread.send_fps.connect(lambda x: self.fps_label.setText(x))
        #裂缝分类
        self.torch_thread.send_input.connect(lambda x: self.showimg(x, self.file_input, 'img'))
        self.torch_thread.send_output.connect(lambda x: self.showimg(x, self.file_output, 'img'))
        self.torch_thread.send_msg.connect(lambda x: self.out_msg(x))
        self.torch_thread.send_title.connect(lambda x: self.out_msg(x))
        #裂缝分割
        self.unet_thread.send_input.connect(lambda x: self.showimg(x, self.pic1, 'img'))
        self.unet_thread.send_output.connect(lambda x: self.showimg(x, self.pic2, 'img'))
        self.unet_thread.send_outpath.connect(lambda x: self.out_path(x))
        self.unet_thread.send_outpaths.connect(lambda x: self.out_paths(x))
        self.btnstop.clicked.connect(self.stop_seg)
        # 运行或停止 检测
        self.playbtn.clicked.connect(self.run_or_continue)
        self.stopbtn.clicked.connect(self.stop)
        self.outer_csv.clicked.connect(self.trace)
        #裂缝分类检测
        self.det_btn.clicked.connect(self.run_class)
        self.over_btn.clicked.connect(self.stop_class)


    # 寻找pt模型
    def search_pt(self):
        pt_list = os.listdir('./ptmodel')
        pt_list = [file for file in pt_list if file.endswith('.pt')]
        pt_list.sort(key=lambda x: os.path.getsize('./ptmodel/' + x))

        if pt_list != self.pt_list:
            self.pt_list = pt_list
            self.comboBox.clear()
            self.comboBox.addItems(self.pt_list)

    # 寻找pth模型
    def search_pth(self):
        pth_list = os.listdir('./checkpoint')
        pth_list = [file for file in pth_list if file.endswith('.pth')]
        pth_list.sort(key=lambda x: os.path.getsize('./checkpoint/' + x))

        if pth_list != self.pth_list:
            self.pth_list = pth_list
            self.select_model.clear()
            self.select_model.addItems(self.pth_list)
    # Conf 和 IoU 变化、latency变化
    def ValueChange(self):
        self.numcon = self.con_slider.value() / 100.0
        self.numiou = self.iou_slider.value() / 100.0
        self.numlatency = self.latency_slider.value()
        self.con_num.setValue(self.numcon)
        self.yolo_thread.conf = self.numcon
        self.iou_num.setValue(self.numiou)
        self.yolo_thread.iou = self.numiou
        self.latency_num.setValue(self.numlatency)
        self.yolo_thread.latency = self.numlatency
    # Model 变化
    def change_model(self, x):
        self.model_type = self.comboBox.currentText()
        self.yolo_thread.weights = "./ptmodel/%s" % self.model_type
    #pth Model变化
    def change_pthmodel(self,x):
        self.pthmodel_type = self.select_model.currentText()
        self.torch_thread.weights = "./checkpoint/%s" % self.pthmodel_type
    # 显示Label图片
    @staticmethod
    def showimg(img, label, flag):
        try:
            if flag == "path":
                img_src = cv2.imdecode(np.fromfile(img, dtype=np.uint8), -1)
            else:
                img_src = img
            ih, iw, _ = img_src.shape
            w = label.geometry().width()
            h = label.geometry().height()
            # keep original aspect ratio
            if iw / w > ih / h:
                scal = w / iw
                nw = w
                nh = int(scal * ih)
                img_src_ = cv2.resize(img_src, (nw, nh))
            else:
                scal = h / ih
                nw = int(scal * iw)
                nh = h
                img_src_ = cv2.resize(img_src, (nw, nh))

            frame = cv2.cvtColor(img_src_, cv2.COLOR_BGR2RGB)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[2] * frame.shape[1],
                         QImage.Format_RGB888)
            label.setPixmap(QPixmap.fromImage(img))

        except Exception as e:
            print(repr(e))

    # 选择照片/视频 并展示
    def Selectfile(self):
        file, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择你要上传的图片/视频",  # 标题
            "./",  # 默认打开路径为当前路径
            "图片/视频类型 (*.jpg *.jpeg *.png *.bmp *.dib  *.jpe  *.jp2 *.mp4)"  # 选择类型过滤项，过滤内容在括号中
        )
        if file == "":
            pass
        else:
            self.inputPath = file
            self.yolo_thread.source=file
            glo.set_value('inputPath', self.inputPath)
            if ".avi" in self.inputPath or ".mp4" in self.inputPath:
                # 显示第一帧
                self.cap = cv2.VideoCapture(self.inputPath)
                ret, frame = self.cap.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.showimg(rgbImage, self.input, 'img')
            else:
                self.showimg(self.inputPath, self.input, 'path')

    # 导入模块
    def Import(self):
        file, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择你要导入的模型",  # 标题
            "./",  # 默认打开路径为当前路径
            "图片/视频类型 (*.pt)"  # 选择类型过滤项，过滤内容在括号中
        )
        if file == "":
            pass
        else:
            shutil.copy(file, self.pt_Path)
            QMessageBox.information(self, '提示', '模块导入成功!')

    # 导出结果
    def Export(self):
        self.OutputDir, _ = QFileDialog.getSaveFileName(
            self,  # 父窗口对象
            "导出图片/视频",  # 标题
            r".",  # 起始目录
            "图片类型 (*.jpg *.jpeg *.png *.bmp *.dib  *.jpe  *.jp2 *.mp4)"  # 选择类型过滤项，过滤内容在括号中
        )
        if self.output == "":
            QMessageBox.warning(self, '提示', '请先选择图片/视频保存的位置')
        else:
            try:
                shutil.copy(self.yolo_thread.save_path, self.OutputDir)
                QMessageBox.warning(self, '提示', '导出成功!')
            except Exception as e:
                QMessageBox.warning(self, '提示', '请先完成识别工作')
                print(e)
    def trace(self):
        self.tracing = True
        glo.set_value('trace', self.tracing)
        self.save_with_object_id = True
        glo.set_value('save_with_object_id', self.save_with_object_id)
        # self.run_or_continue()
    #摄像头函数
    def chose_cam(self):
        try:
            self.stop()
            MessageBox(
                self.CloseButton, title='Tips', text='Loading camera', time=2000, auto=True).exec_()
            # get the number of local cameras
            _, cams = Camera().get_cam_num()
            print(cams)
            popMenu = QMenu()
            popMenu.setFixedWidth(self.camera.width())
            popMenu.setStyleSheet('''
                                                       QMenu {
                                                       font-size: 16px;
                                                       font-family: "Microsoft YaHei UI";
                                                       font-weight: light;
                                                       color:white;
                                                       padding-left: 5px;
                                                       padding-right: 5px;
                                                       padding-top: 4px;
                                                       padding-bottom: 4px;
                                                       border-style: solid;
                                                       border-width: 0px;
                                                       border-color: rgba(255, 255, 255, 255);
                                                       border-radius: 3px;
                                                       background-color: rgba(200, 200, 200,50);}
                                                       ''')

            for cam in cams:
                exec("action_%s = QAction('%s')" % (cam, cam))
                exec("popMenu.addAction(action_%s)" % cam)
                print(cam)
            x = self.result_2.mapToGlobal(self.camera.pos()).x()
            y = self.result_2.mapToGlobal(self.camera.pos()).y()
            y = y + self.camera.frameGeometry().height()
            pos = QPoint(x, y)
            action = popMenu.exec_(pos)
            if action:
                self.yolo_thread.source = action.text()
                # print(self.yolo_thread.source)
                self.statistic_msg('Loading camera：{}'.format(action.text()))
        except Exception as e:
            self.statistic_msg('%s' % e)

    def statistic_msg(self, msg):
        self.outputbox.setText(msg)
        # self.qtimer.start(3000)
    # 最大化最小化窗口
    def max_or_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status:
            self.showMaximized()
            GLOBAL_STATE = False
        else:
            self.showNormal()
            GLOBAL_STATE = True

    # 开始/暂停 预测
    def run_or_continue(self):
        if self.yolo_thread.source.isnumeric():
            self.yolo_thread.jump_out = False
            if self.playbtn.isChecked():
                self.yolo_thread.is_continue = True
                if not self.yolo_thread.isRunning():
                    self.yolo_thread.start()
                s = os.path.basename(self.yolo_thread.source)
                s = 'camera' if s.isnumeric() else s
                self.foot_print('Detecting >> model：{}，file：{}'.
                                format(os.path.basename(self.yolo_thread.weights),
                                       s))
            else:
                self.yolo_thread.is_continue = False
                self.foot_print('Pause')
        else:
            if self.inputPath == "":
                QMessageBox.warning(self, "提示", "请先选择需要识别的图片/视频!")
            else:
                self.yolo_thread.jump_out = False
                if self.playbtn.isChecked():
                    self.yolo_thread.is_continue = True
                    if not self.yolo_thread.isRunning():
                        self.yolo_thread.start()
                    s = os.path.basename(self.yolo_thread.source)
                    s = 'camera' if s.isnumeric() else s
                    self.foot_print('Detecting >> model：{}，file：{}'.
                                        format(os.path.basename(self.yolo_thread.weights),
                                                s))
            # self.foot_print("开始检测>>>>>" + self.inputPath )
                else:
                    self.yolo_thread.is_continue = False
                    self.foot_print('Pause')
    #裂缝分类
    def run_class(self):
        if self.torch_thread.source.isnumeric():
            self.torch_thread.jump_out = False
            if self.det_btn.isChecked():
                self.torch_thread.is_continue = True
                if not self.torch_thread.isRunning():
                    self.torch_thread.start()
                s = os.path.basename(self.torch_thread.source)
                s = 'camera' if s.isnumeric() else s
                self.output_text_path.setPlainText('Detecting >> model：{}，file：{}'.
                                format(os.path.basename(self.torch_thread.weights),
                                       s))
            else:
                self.torch_thread.is_continue = False
        else:
            if self.inputPath == "":
                QMessageBox.warning(self, "提示", "请先选择需要识别的图片/视频!")
            else:
                self.torch_thread.jump_out = False
                if self.det_btn.isChecked():
                    self.output_text_path.setPlainText('')
                    self.output_class.setPlainText('')
                    self.torch_thread.is_continue = True
                    if not self.torch_thread.isRunning():
                        self.torch_thread.start()
                        if(isinstance(self.inputPath, str)):
                            self.output_text_path.appendPlainText("开始检测>>>>>" + os.path.basename(self.inputPath))
                        elif(isinstance(self.inputPath, list)):
                            self.output_text_path.appendPlainText("开始检测>>>>>" + os.path.basename(self.inputPath[0].split('/')[-2])+"文件夹下所有图片")
                else:
                    self.torch_thread.is_continue = False
    #裂缝分割
    def seg_pic(self):
        if self.inputPath == "":
            QMessageBox.warning(self, "提示", "请先选择需要识别的图片/视频!")
        else:
            self.unet_thread.jump_out = False
            if self.segpic.isChecked():
                self.unet_thread.is_continue = True
                if not self.unet_thread.isRunning():
                    self.unet_thread.start()
                    if(isinstance(self.inputPath,str)):
                        self.msgpath.appendPlainText("开始检测>>>>>" + self.inputPath)
                    elif (isinstance(self.inputPath, list)):
                        self.msgpath.appendPlainText("开始检测>>>>>" + self.directory+" 文件夹下的所有图片")
            else:
                self.unet_thread.is_continue = False

    def seg_pics(self):
        if self.inputPath == "":
            QMessageBox.warning(self, "提示", "请先选择需要识别的图片/视频!")
        else:
            self.unet_thread.jump_out = False
            if self.segpics.isChecked():
                self.unet_thread.is_continue = True
                if not self.unet_thread.isRunning():
                    self.unet_thread.start()
                    if(isinstance(self.inputPath,str)):
                        self.msgpath.appendPlainText("开始检测>>>>>" + self.inputPath)
                    elif (isinstance(self.inputPath, list)):
                        self.msgpath.appendPlainText("开始检测>>>>>" + self.directory+" 文件夹下的所有图片")
            else:
                self.unet_thread.is_continue = False
    # 停止识别

    def stop(self):
        self.yolo_thread.jump_out = True
        self.foot_print('Stop')
        self.inputPath=""
        self.tracing = False
        glo.set_value('trace', self.tracing)
        self.save_with_object_id = False
        glo.set_value('save_with_object_id', self.save_with_object_id)
        if self.yolo_thread.source.isnumeric():
            cap = cv2.VideoCapture(self.yolo_thread.source)
            cap.release()
            print(111)
    # 停止分类
    def stop_class(self):
        self.torch_thread.jump_out = True
        self.output_text_path.setPlainText('stop')
        self.inputPath = ""

    # 停止分割
    def stop_seg(self):
        self.unet_thread.jump_out = True
        self.msgpath.setPlainText('stop')
        self.inputPath = ""
        self.outpath.setText('保存图片路径')
        self.outpaths.setText('保存文件夹路径')
        self.picname.setText('上传图片名称')
        self.picsname.setText('打开文件夹名称')
    # 统计结果
    def show_result(self, statistic_dic):
        try:
            self.resultlist.clear()
            s=""
            statistic_dic = sorted(statistic_dic.items(), key=lambda x: x[1], reverse=True)
            statistic_dic = [i for i in statistic_dic if i[1] > 0]
            for i in statistic_dic:
                if(str(i[0])=="Longgitudinal_cracks"):
                    s="纵向裂纹"
                elif(str(i[0])=="DeepLonggitudinal_cracks"):
                    s="纵向分割线"
                elif (str(i[0]) == "Lateral_cracks"):
                    s = "横向裂纹"
                elif (str(i[0]) == "DeepLateral_cracks"):
                    s = "横向分割线"
                elif (str(i[0]) == "Alligator_cracks"):
                    s = "龟裂纹"
                elif (str(i[0]) == "Potholes"):
                    s = "坑洼"
                elif (str(i[0]) == "Zebra_crossing"):
                    s = "斑马线"
                elif (str(i[0]) == "White_line"):
                    s = "白线"
                results = [ s + '：' + str(i[1])]
                self.resultlist.addItems(results)

        except Exception as e:
            print(repr(e))

    # foot栏 输出结果
    def foot_print(self, msg):
        if msg in ['Stop','Finished']:
            self.playbtn.setChecked(False)
        self.outputbox.setText(msg)
    def out_msg(self, msg):
        self.output_class.appendPlainText(msg)
    def out_path(self,path):
        self.outpath.setText(path)
    def out_paths(self,path):
        self.outpaths.setText(path)
    #打开裂缝检测图片
    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择你要上传的图片",  # 标题
            "./",  # 默认打开路径为当前路径
            "单个图片 (*.jpg *.jpeg *.png)"  # 选择类型过滤项，过滤内容在括号中
        )
        if file == "":
            pass
        else:
            self.inputPath = file
            print(file)
            self.output_text_path.setPlainText(file)
            self.torch_thread.source=file
            glo.set_value('inputPath', self.inputPath)
            self.showimg(self.inputPath, self.file_input, 'path')

    #打开多张裂缝检测图片
    def open_files(self):
        file, _ = QFileDialog.getOpenFileNames(self, "打开", "", "多个图片(*.jpg;*.png)")
        # print(self.imgs_name)
        self.inputPath = file

        # print(self.inputPath)
        glo.set_value('inputPath', self.inputPath)
        imgs_name = ''
        for img_name in self.inputPath:
            imgs_name = imgs_name + img_name + '\n'
        self.output_text_path.setPlainText(imgs_name)
        self.torch_thread.source = imgs_name
    #打开视频
    def open_video(self):

        file, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择你要上传的视频",  # 标题
            "./",  # 默认打开路径为当前路径
            "视频类型 (*.mp4)"  # 选择类型过滤项，过滤内容在括号中
        )
        if file == "":
            pass
        else:
            self.inputPath = file
            self.torch_thread.source = file
            glo.set_value('inputPath', self.inputPath)
            if ".avi" in self.inputPath or ".mp4" in self.inputPath:
                # 显示第一帧
                self.cap = cv2.VideoCapture(self.inputPath)
                ret, frame = self.cap.read()
                if ret:
                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.showimg(rgbImage, self.file_input, 'img')
                    self.output_text_path.setPlainText(file)
            else:
                self.showimg(self.inputPath, self.file_input, 'path')
    def open_camera(self):
        try:
            self.stop_class()
            MessageBox(
                self.CloseButton, title='Tips', text='Loading camera', time=2000, auto=True).exec_()
            # get the number of local cameras
            _, cams = Camera().get_cam_num()
            print(cams)
            popMenu = QMenu()
            popMenu.setFixedWidth(self.camera.width())
            popMenu.setStyleSheet('''
                                                       QMenu {
                                                       font-size: 16px;
                                                       font-family: "Microsoft YaHei UI";
                                                       font-weight: light;
                                                       color:white;
                                                       padding-left: 5px;
                                                       padding-right: 5px;
                                                       padding-top: 4px;
                                                       padding-bottom: 4px;
                                                       border-style: solid;
                                                       border-width: 0px;
                                                       border-color: rgba(255, 255, 255, 255);
                                                       border-radius: 3px;
                                                       background-color: rgba(200, 200, 200,50);}
                                                       ''')

            for cam in cams:
                exec("action_%s = QAction('%s')" % (cam, cam))
                exec("popMenu.addAction(action_%s)" % cam)
                # print(cam)
            x = self.result_2.mapToGlobal(self.camera.pos()).x()
            y = self.result_2.mapToGlobal(self.camera.pos()).y()
            y = y + self.camera.frameGeometry().height()
            pos = QPoint(x, y)
            action = popMenu.exec_(pos)
            if action:
                self.torch_thread.source = action.text()
                glo.set_value('so',self.torch_thread.source)
                print(self.torch_thread.source)
                self.output_text_path.setPlainText('Loading camera：{}'.format(action.text()))
        except Exception as e:
            self.output_text_path.setPlainText('%s' % e)

    #裂缝分割界面
    def open_pic(self):
        file, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择你要上传的图片",  # 标题
            "./",  # 默认打开路径为当前路径
            "单个图片 (*.jpg *.jpeg *.png)"  # 选择类型过滤项，过滤内容在括号中
        )
        if file == "":
            pass
        else:
            self.inputPath = file
            print(file)
            self.picname.setText(os.path.basename(file))
            # self.torch_thread.source = file
            self.msgpath.setPlainText(file)
            glo.set_value('inputPath', self.inputPath)
            self.showimg(self.inputPath, self.pic1, 'path')

    def open_pics(self):
        directory1 = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "./")  # 起始路径
        # print(self.imgs_name)
        self.directory=directory1
        self.picsname.setText(os.path.basename(directory1))
        glo.set_value('directory', self.directory)
        img_total = []
        imgfile = os.listdir(directory1)
        for filename in imgfile:
            name, type = os.path.splitext(filename)
            if type == ('.jpg' or '.png'):
                img_total.append(filename)
        self.inputPath = img_total
        print(self.inputPath)
        glo.set_value('inputPath', self.inputPath)
        imgs_name = ''
        for img_name in self.inputPath:
            imgs_name = imgs_name + img_name + '\n'
        self.msgpath.setPlainText(imgs_name)
class MyWindow(YOLO):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.center()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.mouse_start_pt = event.globalPosition().toPoint()
            self.window_pos = self.frameGeometry().topLeft()
            self.drag = True

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.drag:
            distance = event.globalPosition().toPoint() - self.mouse_start_pt
            self.move(self.window_pos + distance)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.drag = False

    def center(self):
        # PyQt6获取屏幕参数
        screen = QGuiApplication.primaryScreen().size()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2 - 10)

    # def open_file(self):
    #     self.img_name = QFileDialog.getOpenFileName(self, "打开", "", "图片(*.jpg;*.png)")
    #     # ui.file_name.setPlainText(self.img_name[0])
    #     # self.img_opened = True
