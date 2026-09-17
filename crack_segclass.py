# -*- codeing:utf-8 -*-
"""
作者：86156
日期：2023年04月23日
"""
import os
import time
# import matplotlib
# matplotlib.use('TkAgg')
import cv2
import matplotlib.pyplot as plt
import torch
from tkinter import *
import shutil
import torchvision
import torch.nn.functional as F
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import pandas as pd
from torchvision import transforms
from PIL import Image
from PySide6.QtCore import QThread
from PySide6.QtCore import Signal
from lib import glo
import gc
import mmcv
import os.path as osp
from Model.unet_model import UNet
class UnetThread(QThread):
    send_input = Signal(np.ndarray)
    send_output = Signal(np.ndarray)
    send_msg = Signal(str)
    send_outpath = Signal(str)
    send_outpaths = Signal(str)
    def __init__(self):
        super(UnetThread, self).__init__()
        self.weights = './umodel/best_model_2.pth'
        self.source = '0'
        self.is_continue = True  # continue/pause
        self.jump_out = False  # jump out of the loop
        # 图片读取进程
        self.output_size = 480
        # self.img2predict = ""
        # # 初始化视频读取线程
        self.origin_shape = ()


    @torch.no_grad()
    def run(self,
            device='',
            ):
        try:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            # 加载网络，图片单通道，分类为1。
            net = UNet(n_channels=1, n_classes=1)
            # 将网络拷贝到deivce中
            net.to(device=device)
            # 加载模型参数
            net.load_state_dict(torch.load(self.weights, map_location=device))  # todo 模型位置
            # 测试模式
            net.eval()
            self.model = net
            if self.jump_out:
                self.send_path.emit('检测已经停止')
            else:
                if self.is_continue:
                    # 载入一张测试图像路径
                    img_path = glo.get_value('inputPath')
                    if (isinstance(img_path, str)):
                        suffix = img_path.split("/")[-1]
                        save_path = osp.join("unetimg", suffix)
                        shutil.copy(img_path, save_path)
                        # 应该调整一下图片的大小，然后统一防在一起
                        im0 = cv2.imread(save_path)
                        resize_scale = self.output_size / im0.shape[0]
                        im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
                        cv2.imwrite(save_path, im0)
                        self.origin_shape = (im0.shape[1], im0.shape[0])
                        #检测
                        img = cv2.imread(save_path)
                        # 转为灰度图
                        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                        img = cv2.resize(img, (512, 512))
                        # 转为batch为1，通道为1，大小为512*512的数组
                        img = img.reshape(1, 1, img.shape[0], img.shape[1])
                        # 转为tensor
                        img_tensor = torch.from_numpy(img)
                        # 将tensor拷贝到device中，只用cpu就是拷贝到cpu中，用cuda就是拷贝到cuda中。
                        img_tensor = img_tensor.to(device=device, dtype=torch.float32)
                        # 预测
                        pred = self.model(img_tensor)
                        # 提取结果
                        pred = np.array(pred.data.cpu()[0])[0]
                        # 处理结果
                        pred[pred >= 0.5] = 255
                        pred[pred < 0.5] = 0
                        # 保存图片
                        im0 = cv2.resize(pred, self.origin_shape)
                        folder_path = './unetimg/test/'+suffix
                        self.send_outpath.emit(folder_path)
                        cv2.imwrite(folder_path, im0)
                        with Image.open(folder_path) as img:
                            if img.mode == 'L':  # check if single channel
                                img = img.convert('RGB')  # convert to 3 channel
                                img.save(folder_path)  # overwrite original file
                        im_array = np.array(img)
                        self.send_output.emit(im_array)
                    elif (isinstance(img_path, list)):
                        imgs_root=glo.get_value('directory')
                        print(imgs_root)
                        assert os.path.exists(imgs_root), f"file: '{imgs_root}' dose not exist."
                        img_path_list = [os.path.join(imgs_root, i) for i in os.listdir(imgs_root) if i.endswith(".jpg")]
                        print(img_path_list)
                        for img_one in img_path_list:
                            assert os.path.exists(img_one), f"file: '{img_one}' dose not exist."
                            print(img_one)
                            img_one = str(img_one).replace('\\', '/')
                            print(img_one)
                            save_path = osp.join("unetimg", osp.basename(img_one))
                            print(osp.basename(img_one))
                            shutil.copy(img_one, save_path)
                            # 应该调整一下图片的大小，然后统一防在一起
                            im0 = cv2.imread(save_path)
                            resize_scale = self.output_size / im0.shape[0]
                            im0 = cv2.resize(im0, (0, 0), fx=resize_scale, fy=resize_scale)
                            cv2.imwrite(save_path, im0)
                            im_array = np.array(im0)
                            self.send_input.emit(im_array)

                            self.origin_shape = (im0.shape[1], im0.shape[0])
                            # 检测
                            img = cv2.imread(save_path)
                            # 转为灰度图
                            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                            img = cv2.resize(img, (512, 512))
                            # 转为batch为1，通道为1，大小为512*512的数组
                            img = img.reshape(1, 1, img.shape[0], img.shape[1])
                            # 转为tensor
                            img_tensor = torch.from_numpy(img)
                            # 将tensor拷贝到device中，只用cpu就是拷贝到cpu中，用cuda就是拷贝到cuda中。
                            img_tensor = img_tensor.to(device=device, dtype=torch.float32)
                            # 预测
                            pred = self.model(img_tensor)
                            # 提取结果
                            pred = np.array(pred.data.cpu()[0])[0]
                            # 处理结果
                            pred[pred >= 0.5] = 255
                            pred[pred < 0.5] = 0
                            # 保存图片
                            im0 = cv2.resize(pred, self.origin_shape)
                            folder_path = './unetimg/test/' + osp.basename(img_one)
                            self.send_outpaths.emit(folder_path)
                            cv2.imwrite(folder_path, im0)
                            with Image.open(folder_path) as img:
                                if img.mode == 'L':  # check if single channel
                                    img = img.convert('RGB')  # convert to 3 channel
                                    img.save(folder_path)  # overwrite original file
                            im_array = np.array(img)
                            self.send_output.emit(im_array)
                            time.sleep(1)


        except Exception as e:
            self.send_msg.emit("程序出错啦!!!   " + str(e))
