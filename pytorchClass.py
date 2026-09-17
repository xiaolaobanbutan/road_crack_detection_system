# -*- codeing:utf-8 -*-
"""
作者：86156
日期：2023年04月13日
"""
import os
import time
# import matplotlib
# matplotlib.use('TkAgg')
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
from pathlib import Path

FONT_PATH = Path(__file__).resolve().parent / "Font" / "FiraMono-Medium.otf"

class PytorchThread(QThread):
    send_input = Signal(np.ndarray)
    send_output = Signal(np.ndarray)
    # emit：detecting/pause/stop/finished/error msg
    send_msg = Signal(str)
    send_title=Signal(str)
    def __init__(self):
        super(PytorchThread, self).__init__()
        self.weights = './checkpoint/best6-0.839.pth'
        self.current_weight = './checkpoint/best6-0.839.pth'
        self.source = ''
        self.is_continue = True  # continue/pause
        self.jump_out = False  # jump out of the loop
        # windows操作系统
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


    @torch.no_grad()
    def run(self,
               device='',
               font='',
               idx_to_labels={}#类别
               ):
        try:
            # 有 GPU 就用 GPU，没有就用 CPU
            device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
            # 导入中文字体，指定字号
            font = ImageFont.truetype(str(FONT_PATH), 30)
            # 载入类别
            if self.weights=='./checkpoint/crack5_fenge_92.593.pth':
                idx_to_labels = np.load('idx_to_labels1.npy', allow_pickle=True).item()
            else:
                idx_to_labels = np.load('idx_to_labels.npy', allow_pickle=True).item()
            # 导入训练好的模型

            model = torch.load(self.weights)
            model = model.eval().to(device)
            # 预处理
            # 测试集图像预处理-RCTN：缩放、裁剪、转 Tensor、归一化
            test_transform = transforms.Compose([transforms.Resize(256),
                                                 transforms.CenterCrop(224),
                                                 transforms.ToTensor(),
                                                 transforms.Normalize(
                                                     mean=[0.485, 0.456, 0.406],
                                                     std=[0.229, 0.224, 0.225])
                                                 ])
            import cv2
            import time
            # 停止检测
            if self.jump_out:
                self.send_msg.emit('检测已经停止')
            else:
                if (self.source.isnumeric()):
                    # 获取摄像头，传入0表示获取系统默认摄像头
                    # 处理帧函数
                    def process_frame(img):
                        # 记录该帧开始处理的时间
                        start_time = time.time()
                        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR转RGB
                        img_pil = Image.fromarray(img_rgb)  # array 转 PIL
                        input_img = test_transform(img_pil).unsqueeze(0).to(device)  # 预处理
                        pred_logits = model(input_img)  # 执行前向预测，得到所有类别的 logit 预测分数
                        pred_softmax = F.softmax(pred_logits, dim=1)  # 对 logit 分数做 softmax 运算

                        top_n = torch.topk(pred_softmax, 4)  # 取置信度最大的 n 个结果
                        pred_ids = top_n[1].cpu().detach().numpy().squeeze()  # 解析预测类别
                        confs = top_n[0].cpu().detach().numpy().squeeze()  # 解析置信度
                        # 使用PIL绘制中文
                        draw = ImageDraw.Draw(img_pil)
                        # 在图像上写字
                        for i in range(len(confs)):
                            pred_class = idx_to_labels[pred_ids[i]]
                            text = '{:<15} {:>.3f}'.format(pred_class, confs[i])
                            # 文字坐标，中文字符串，字体，bgra颜色
                            draw.text((50, 100 + 50 * i), text, font=font, fill=(255, 0, 0, 1))
                        img = np.array(img_pil)  # PIL 转 array
                        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # RGB转BGR
                        # 记录该帧处理完毕的时间
                        end_time = time.time()
                        # 计算每秒处理图像帧数FPS
                        FPS = 1 / (end_time - start_time)
                        # 图片，添加的文字，左上角坐标，字体，字体大小，颜色，线宽，线型
                        img = cv2.putText(img, 'FPS  ' + str(int(FPS)), (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                          (255, 0, 255), 4,
                                          cv2.LINE_AA)
                        # im_array0 = np.array(img)
                        # self.send_input.emit(img)
                        return img
                    # 调用摄像头获取每帧（模板）
                    # 调用摄像头逐帧实时处理模板
                    # 不需修改任何代码，只需修改process_frame函数即可
                    # 获取摄像头，传入0表示获取系统默认摄像头
                    # print(type(glo.get_value('so')))
                    so=glo.get_value('so')
                    # print(type(so))
                    cap = cv2.VideoCapture(int(so))
                    # 打开cap
                    cap.open(int(so))
                    # 无限循环，直到break被触发
                    while cap.isOpened():
                        # 获取画面
                        success, frame = cap.read()
                        if not success:
                            print('Error')
                            break

                        ## !!!处理帧函数
                        frame = process_frame(frame)

                        # 展示处理后的三通道图像
                        cv2.imshow('my_window', frame)

                        if cv2.waitKey(1) in [ord('q'), 27]:  # 按键盘上的q或esc退出（在英文输入法下）
                            break

                    # 关闭摄像头
                    cap.release()
                    self.source=''
                    # 关闭图像窗口
                    cv2.destroyAllWindows()
                else:
                    if self.is_continue:
                        # 载入一张测试图像路径
                        img_path = glo.get_value('inputPath')
                        # print(type(img_path))
                        #根据img_path的类型判断是否为多张图片
                        if(isinstance(img_path, str) ):
                            img_end=os.path.basename(img_path)
                            print(img_end)
                            name, type = os.path.splitext(img_end)
                            print(type)
                            if type == ('.jpg' or '.png'):
                                img_pil = Image.open(img_path)
                                print(img_pil)
                                # 预处理、前向预测
                                input_img = test_transform(img_pil)  # 预处理
                                # input_img.shape
                                input_img = input_img.unsqueeze(0).to(device)
                                # 执行前向预测，得到所有类别的 logit 预测分数
                                pred_logits = model(input_img)
                                pred_softmax = F.softmax(pred_logits, dim=1)  # 对 logit 分数做 softmax 运算
                                # plt.figure(figsize=(22, 10))
                                x = idx_to_labels.values()
                                y = pred_softmax.cpu().detach().numpy()[0] * 100
                                width = 0.45  # 柱状图宽度
                                ax = plt.bar(x, y, width)

                                # plt.bar_label(ax, fmt='%.2f', fontsize=15)  # 置信度数值
                                # plt.tick_params(labelsize=20)  # 设置坐标文字大小
                                # plt.title(os.path.basename(img_path), fontsize=20)
                                # plt.xticks(rotation=20)  # 横轴文字旋转
                                # plt.xlabel('类别', fontsize=20)
                                # plt.ylabel('置信度', fontsize=20)
                                # plt.show()
                                # 置信度最大的前 n 个结果
                                n = 4
                                top_n = torch.topk(pred_softmax, n)  # 取置信度最大的 n 个结果
                                pred_ids = top_n[1].cpu().detach().numpy().squeeze()  # 解析出类别
                                confs = top_n[0].cpu().detach().numpy().squeeze()  # 解析出置信度
                                # 图像分类结果写在原图上
                                draw = ImageDraw.Draw(img_pil)
                                for i in range(n):
                                    class_name = idx_to_labels[pred_ids[i]]  # 获取类别名称
                                    confidence = confs[i] * 100  # 获取置信度
                                    text = '{:<6} {:>.3f}'.format(class_name, confidence)  # 保留 4 位小数
                                    print(text)
                                    # self.output_class.setPlainText(text)
                                    # 文字坐标，中文字符串，字体，rgba颜色
                                    draw.text((20, 20+40 * i), text, font=font, fill=(255, 0, 0, 1))
                                # img_pil
                                img_pil.save('./output/{}'.format(os.path.basename(img_path)))
                                im_array = np.array(img_pil)
                                self.send_input.emit(im_array)
                                print('111')
                                fig = plt.figure(figsize=(25, 15))
                                # 绘制左图-预测图
                                # 绘制右图-柱状图
                                ax2 = plt.subplot(1, 1, 1)
                                x = idx_to_labels.values()
                                y = pred_softmax.cpu().detach().numpy()[0] * 100
                                ax2.bar(x, y, alpha=0.5, width=0.3, color='yellow', edgecolor='red', lw=3)
                                plt.bar_label(ax, fmt='%.2f', fontsize=40)  # 置信度数值
                                plt.title('{} 图像分类预测结果'.format(os.path.basename(img_path)), fontsize=50)
                                plt.xlabel('类别', fontsize=40)
                                plt.ylabel('置信度', fontsize=40)
                                plt.ylim([0, 110])  # y轴取值范围
                                ax2.tick_params(labelsize=40)  # 坐标文字大小
                                plt.xticks(rotation=0)  # 横轴文字旋转
                                plt.tight_layout()
                                fig.savefig('图表/{}'.format(os.path.basename(img_path)))
                                img_det = Image.open('图表/{}'.format(os.path.basename(img_path)))
                                im_array = np.array(img_det)
                                self.send_output.emit(im_array)
                                s2 = '类别       类别序号       置信度(%)'
                                self.send_title.emit(s2)
                                pred_df = pd.DataFrame()  # 预测结果表格
                                for i in range(n):
                                    class_name = idx_to_labels[pred_ids[i]]  # 获取类别名称
                                    label_idx = int(pred_ids[i])  # 获取类别号
                                    confidence = confs[i] * 100  # 获取置信度
                                    pred_df = pred_df.append({'Class': class_name, 'Class_ID': label_idx, 'Confidence(%)': confidence},
                                                             ignore_index=True)  # 预测结果表格添加一行
                                    self.send_msg.emit('{}        {}       {}'.format(class_name,label_idx,confidence))
                                print(pred_df)
                            elif type == ('.mp4'):
                                # 图像分类预测函数（同上个教程）
                                def pred_single_frame(img, n=5):
                                    '''
                                    输入摄像头画面bgr-array，输出前n个图像分类预测结果的图像bgr-array
                                    '''
                                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR 转 RGB
                                    img_pil = Image.fromarray(img_rgb)  # array 转 pil
                                    input_img = test_transform(img_pil).unsqueeze(0).to(device)  # 预处理
                                    pred_logits = model(input_img)  # 执行前向预测，得到所有类别的 logit 预测分数
                                    pred_softmax = F.softmax(pred_logits, dim=1)  # 对 logit 分数做 softmax 运算

                                    top_n = torch.topk(pred_softmax, n)  # 取置信度最大的 n 个结果
                                    pred_ids = top_n[1].cpu().detach().numpy().squeeze()  # 解析出类别
                                    confs = top_n[0].cpu().detach().numpy().squeeze()  # 解析出置信度

                                    # 在图像上写字
                                    draw = ImageDraw.Draw(img_pil)
                                    # 在图像上写字
                                    for i in range(len(confs)):
                                        pred_class = idx_to_labels[pred_ids[i]]
                                        text = '{:<15} {:>.3f}'.format(pred_class, confs[i])
                                        # 文字坐标，中文字符串，字体，rgba颜色
                                        draw.text((50, 100 + 50 * i), text, font=ImageFont.truetype(str(FONT_PATH), 40), fill=(255, 0, 0, 1))

                                    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)  # RGB转BGR
                                    img_arry=np.array(img_pil)
                                    self.send_input.emit(img_arry)
                                    return img_bgr, pred_softmax

                                output_path = 'output/{}'.format(os.path.basename(img_path))
                                # 创建临时文件夹，存放每帧结果
                                temp_out_dir = time.strftime('%Y%m%d%H%M%S')
                                os.mkdir(temp_out_dir)
                                print('创建临时文件夹 {} 用于存放每帧预测结果'.format(temp_out_dir))
                                # 读入待预测视频
                                imgs = mmcv.VideoReader(img_path)

                                prog_bar = mmcv.ProgressBar(len(imgs))
                                # 对视频逐帧处理
                                for frame_id, img in enumerate(imgs):
                                    ## 处理单帧画面
                                    img, pred_softmax = pred_single_frame(img, n=4)
                                    # 将处理后的该帧画面图像文件，保存至 /tmp 目录下
                                    cv2.imwrite(f'{temp_out_dir}/{frame_id:06d}.jpg', img)
                                    prog_bar.update()  # 更新进度条

                                # 把每一帧串成视频文件
                                mmcv.frames2video(temp_out_dir, output_path, fps=imgs.fps, fourcc='mp4v')

                                shutil.rmtree(temp_out_dir)  # 删除存放每帧画面的临时文件夹
                                print('删除临时文件夹', temp_out_dir)
                                print('视频已生成', output_path)
                        elif(isinstance(img_path, list)):
                            # load image
                            # 指向需要遍历预测的图像文件夹
                            # print(img_path[0].split('/')[-2])
                            imgs_root = "./{}".format(img_path[0].split('/')[-2])
                            assert os.path.exists(imgs_root), f"file: '{imgs_root}' dose not exist."
                            # # # 读取指定文件夹下所有jpg图像路径
                            img_path_list = [os.path.join(imgs_root, i) for i in os.listdir(imgs_root) if i.endswith(".jpg")]
                            # print(img_path_list)
                            for img_one in img_path_list:
                                assert os.path.exists(img_one), f"file: '{img_one}' dose not exist."
                                print(img_one)
                                img_one = str(img_one).replace('\\', '/')
                                print(img_one)
                                img_pil = Image.open(img_one)
                                # 预处理、前向预测
                                input_img = test_transform(img_pil)  # 预处理
                                # input_img.shape
                                input_img = input_img.unsqueeze(0).to(device)
                                # 执行前向预测，得到所有类别的 logit 预测分数
                                pred_logits = model(input_img)
                                pred_softmax = F.softmax(pred_logits, dim=1)  # 对 logit 分数做 softmax 运算
                                x = idx_to_labels.values()
                                y = pred_softmax.cpu().detach().numpy()[0] * 100
                                width = 0.45  # 柱状图宽度
                                ax = plt.bar(x, y, width)
                                # 置信度最大的前 n 个结果
                                n = 4
                                top_n = torch.topk(pred_softmax, n)  # 取置信度最大的 n 个结果
                                pred_ids = top_n[1].cpu().detach().numpy().squeeze()  # 解析出类别
                                confs = top_n[0].cpu().detach().numpy().squeeze()  # 解析出置信度
                                draw = ImageDraw.Draw(img_pil)
                                for i in range(n):
                                    class_name = idx_to_labels[pred_ids[i]]  # 获取类别名称
                                    confidence = confs[i] * 100  # 获取置信度
                                    text = '{:<6} {:>.3f}'.format(class_name, confidence)  # 保留 4 位小数
                                    print(text)
                                    # self.output_class.setPlainText(text)
                                    # 文字坐标，中文字符串，字体，rgba颜色
                                    draw.text((20, 20 + 40 * i), text, font=font, fill=(255, 0, 0, 1))
                                # img_pil
                                img_pil.save('./output/{}'.format(os.path.basename(img_one)))
                                im_array = np.array(img_pil)
                                self.send_input.emit(im_array)
                                fig = plt.figure(figsize=(25, 15))
                                # 绘制左图-预测图
                                # 绘制右图-柱状图
                                ax2 = plt.subplot(1, 1, 1)
                                x = idx_to_labels.values()
                                y = pred_softmax.cpu().detach().numpy()[0] * 100
                                ax2.bar(x, y, alpha=0.5, width=0.3, color='yellow', edgecolor='red', lw=3)
                                plt.bar_label(ax, fmt='%.2f', fontsize=40)  # 置信度数值
                                plt.title('{} 图像分类预测结果'.format(os.path.basename(img_one)), fontsize=50)
                                plt.xlabel('类别', fontsize=40)
                                plt.ylabel('置信度', fontsize=40)
                                plt.ylim([0, 110])  # y轴取值范围
                                ax2.tick_params(labelsize=40)  # 坐标文字大小
                                plt.xticks(rotation=0)  # 横轴文字旋转
                                plt.tight_layout()
                                fig.savefig('图表/{}'.format(os.path.basename(img_one)))
                                img_det = Image.open('图表/{}'.format(os.path.basename(img_one)))
                                im_array = np.array(img_det)
                                self.send_output.emit(im_array)
                                s2 = '类别       类别序号       置信度(%)'
                                self.send_title.emit(s2)
                                pred_df = pd.DataFrame()  # 预测结果表格
                                for i in range(n):
                                    class_name = idx_to_labels[pred_ids[i]]  # 获取类别名称
                                    label_idx = int(pred_ids[i])  # 获取类别号
                                    confidence = confs[i] * 100  # 获取置信度
                                    pred_df = pred_df.append(
                                        {'Class': class_name, 'Class_ID': label_idx, 'Confidence(%)': confidence},
                                        ignore_index=True)  # 预测结果表格添加一行
                                    self.send_msg.emit('{}        {}       {}'.format(class_name, label_idx, confidence))
                                print(pred_df)
                                # time.sleep(1)
        except Exception as e:
            self.send_msg.emit("程序出错啦!!!   " + str(e))