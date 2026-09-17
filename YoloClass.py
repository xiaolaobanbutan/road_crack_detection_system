import argparse
import os
import time
from pathlib import Path
from PySide6.QtCore import Signal
import cv2
import numpy as np
import pandas as pd
import torch
import torch.backends.cudnn as cudnn
from PySide6.QtCore import QThread
from numpy import random
from models.experimental import attempt_load
from utils.datasets import LoadImages,LoadWebcam,LoadStreams
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel
from lib import glo
from sort import *
from random import randint
import csv


class YoloThread(QThread):
    send_input = Signal(np.ndarray)
    send_output = Signal(np.ndarray)
    send_result = Signal(dict)
    # emit：detecting/pause/stop/finished/error msg
    send_msg = Signal(str)
    send_percent = Signal(int)
    send_fps = Signal(str)

    def __init__(self):
        super(YoloThread, self).__init__()
        self.weights = './ptmodel/yolov7.pt'
        self.current_weight = './ptmodel/yolov7.pt'
        self.source = ''
        self.conf = 0.25
        self.iou = 0.40
        self.latency = 0
        self.is_continue = True  # continue/pause
        self.jump_out = False  # jump out of the loop
        self.percent_length = 1000  # progress bar

    # 截取图片(图片路径，坐标信息路径，保存路径)根据检测框坐标截取图片
    @staticmethod
    def CropImage4File(img_path, label_path, save_path):
        img_total = []
        label_total = []
        imgfile = os.listdir(img_path)  # 列出文件路径中的所有路径或文件
        labelfile = os.listdir(label_path)
        for filename in imgfile:
            name, type = os.path.splitext(filename)
            if type == ('.jpg' or '.png'):
                img_total.append(name)
        for filename in labelfile:
            name, type = os.path.splitext(filename)
            if type == '.txt':
                label_total.append(name)
        for _img in img_total:
            if _img in label_total:
                filename_img = _img + '.jpg'
                path = os.path.join(img_path, filename_img)
                img = cv2.imread(path)  # 读取图片，结果为三维数组
                filename_label = _img + '.txt'
                n = 1
                # 打开文件，编码格式'utf-8','r+'读写
                with open(os.path.join(label_path, filename_label), "r+", encoding='utf-8', errors="ignor") as f:
                    for line in f:
                        numbers = line.split(" ")  # 根据空格切割字符串，最后得到的是一个list
                        numbers_float = list(map(float, numbers[1:]))  # 将字符串转化为浮点数
                        numbers_int = np.array(numbers_float, dtype=np.int)  # 将浮点数数组转换为整型数组
                        x1 = int(float(numbers_int[0]))  # x_center - width/2
                        y1 = int(float(numbers_int[1]))  # y_center - height/2
                        x2 = int(float(numbers_int[2]))  # x_center + width/2
                        y2 = int(float(numbers_int[3]))  # y_center + height/2
                        filename_last = _img + "_" + str(numbers[0]) + str(n) + ".jpg"
                        print(filename_last)
                        img_roi = img[y1:y2, x1:x2]  # 剪裁，roi:region of interest
                        cv2.imwrite(os.path.join(save_path, filename_last), img_roi)
                        n = n + 1
            else:
                continue
    #将一段视频按照一定帧数截图
    @staticmethod
    def video_to_frames(path, dir, file, savepath):
        # VideoCapture视频读取类
        # 抽取帧数
        videoCapture = cv2.VideoCapture()
        videoCapture.open(path)
        # 将视频名称切分为名字和后缀MP4，放在一个列表里面
        file = file.split('.mp4')
        # 将列表里面的第一个元素取出来，就是不带后缀的名字
        file = file[0]
        n = 1
        # 30帧一秒，则此处为3秒切一次
        frametime = 5
        # 取出总帧数
        frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)

        for i in range(int(frames)):
            # ret是一个bool类型的数，当为True的时候将这帧照片取出保存在frame里面，反之不取出。
            ret, frame = videoCapture.read()
            if i % frametime == 0:
                # 截取的图片的绝对路径，这里我们要建立一个保存图片的文件夹，例如D:/截图，这里是将图片放在一个文件夹下
                # filename = 'D:/截图' + '/' + file + '_' + str(n) + '.jpg'
                # 如果不想将图片放在一个文件下，而是和源文件一样的目录结构用下面代码
                filename = savepath + '/' + dir + '/' + file + '_' + str(n * 5) + '.jpg'
                folder = savepath + '/' + dir
                if not os.path.exists(folder):  # 判断是否存在文件夹如果不存在则创建为文件夹
                    os.makedirs(folder)

                # 将截取视频的图片保存到绝对路径下面
                cv2.imencode('.jpg', frame)[1].tofile(filename)
                # print(filename)
                n += 1
    @torch.no_grad()
    def run(self,
            imgsz=640,
            device='',
            view_img=False,
            save_conf=False,
            nosave=False,
            classes=None,
            agnostic_nms=False,
            augment=False,
            update=False,
            project='result',
            name='exp',
            exist_ok=False,
            no_trace=False,
            # half = False,
            colored_trk=False,
            save_txt=False,
            save_with_object_id=False,
            save_bbox_dim=False,
            tracing=False,
            csvname='',
            # ....Initialize SORT...
            sort_max_age=5,
            sort_min_hits=2,
            sort_iou_thresh=0.2,
            ):
        # ............................... Bounding Boxes Drawing ............................
        """Function to Draw Bounding boxes"""

        def draw_boxes(img, bbox, identities=None, categories=None, names=None, save_with_object_id=False, path=None,
                       offset=(0, 0)):
            for i, box in enumerate(bbox):
                x1, y1, x2, y2 = [int(i) for i in box]
                x1 += offset[0]
                x2 += offset[0]
                y1 += offset[1]
                y2 += offset[1]
                cat = int(categories[i]) if categories is not None else 0
                id = int(identities[i]) if identities is not None else 0
                data = (int((box[0] + box[2]) / 2), (int((box[1] + box[3]) / 2)))
                label = str(id) + ":" + names[cat]
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 20), 2)
                cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), (255, 144, 30), -1)
                cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, [255, 255, 255], 1)
                # cv2.circle(img, data, 6, color,-1)   #centroid of box
                txt_str = ""
                if save_with_object_id:
                    txt_str += "%i %i %.2f %.2f %i %i %i %i" % (
                        id, cat, round((((box[2] - box[0])/img.shape[1]) ** 2 + ((box[3] - box[1])/img.shape[0])** 2) ** 0.5, 2),
                        round(abs((box[3] - box[1])/img.shape[0]) * abs((box[2] - box[0])/img.shape[1]), 2), int(box[0]), int(box[1]), int(box[2]),
                        int(box[3]))
                    txt_str += "\n"
                    with open(path + '.txt', 'a',encoding='utf-8') as f:
                        f.write(txt_str)
            return img

        # ..............................................................................
        # Initialize

        # Initialize
        try:
            #
            sort_tracker = Sort(max_age=sort_max_age,
                                min_hits=sort_min_hits,
                                iou_threshold=sort_iou_thresh)
            #
            # ........Rand Color for every trk.......
            rand_color_list = []
            for i in range(0, 5005):
                r = randint(0, 255)
                g = randint(0, 255)
                b = randint(0, 255)
                rand_color = (r, g, b)
                rand_color_list.append(rand_color)
            # ......................................
            device = select_device(device)
            half = False
            # Load model
            model = attempt_load(self.weights, map_location=device)  # load FP32 model
            stride = int(model.stride.max())  # model stride
            imgsz = check_img_size(imgsz, s=stride)  # check img_size
            tracing = glo.get_value(('trace'))
            # print(tracing)
            ps = glo.get_value('inputPath')
            save_with_object_id=glo.get_value(('save_with_object_id'))
            save_img = not nosave and not self.source.endswith('.txt')  # save inference images
            # Directories
            save_dir = Path(increment_path(Path(project) / name, exist_ok=exist_ok))  # increment run
            # save_dir.mkdir(parents=True, exist_ok=True)  # make dir
            # 新增
            (save_dir / 'labels' if save_txt or save_with_object_id else save_dir).mkdir(parents=True,
                                                                                         exist_ok=True)  # make dir
            # Set Dataloader
            vid_path, self.vid_writer = None, None

            if half:
                model.half()  # to FP16
            # source
            if (self.source.isnumeric()):
                view_img = check_imshow()
                cudnn.benchmark = True  # set True to speed up constant image size inference
                dataset = LoadStreams(self.source, img_size=imgsz, stride=stride)
            else:
                # half = device.type != 'cpu'  # half precision only supported on CUDA
                # bs = len(dataset)  # batch_size

                dataset = LoadImages(ps, img_size=imgsz, stride=stride)
            # Get names and colors
            names = model.module.names if hasattr(model, 'module') else model.names
            colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

            # Run inference
            if device.type != 'cpu':
                model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
            old_img_w = old_img_h = imgsz
            old_img_b = 1

            dataset = iter(dataset)

            # 参数设置
            start_time = time.time()
            count = 0
            # 开始处理每一张图片
            while True:
                # 停止检测
                if self.jump_out:
                    self.send_percent.emit(0)
                    if self.vid_cap is not None:
                        self.vid_cap.release()
                    self.send_msg.emit('Stop')
                    if self.vid_writer is not None:
                        self.vid_writer.release()
                    break

                # change model
                if self.current_weight != self.weights:
                    # Load model
                    model = attempt_load(self.weights, map_location=device)  # load FP32 model
                    stride = int(model.stride.max())  # model stride
                    imgsz = check_img_size(imgsz, s=stride)  # check img_size
                    if half:
                        model.half()  # to FP16
                    # Get names and colors
                    names = model.module.names if hasattr(model, 'module') else model.names
                    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
                    # Run inference
                    if device.type != 'cpu':
                        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
                    old_img_w = old_img_h = imgsz
                    old_img_b = 1
                    self.current_weight = self.weights

                if self.is_continue:
                    path, img, im0s, self.vid_cap = next(dataset)
                    # print(path)
                    # 原始图片送入 input框
                    self.send_input.emit(im0s if isinstance(im0s, np.ndarray) else im0s[0])
                    # 处理processBar
                    count += 1
                    if count % 30 == 0 and count >= 30:
                        fps = int(30 / (time.time() - start_time))
                        self.send_fps.emit('fps：' + str(fps))
                        start_time = time.time()
                    if self.vid_cap:
                        percent = int(count / self.vid_cap.get(cv2.CAP_PROP_FRAME_COUNT) * self.percent_length)
                        self.send_percent.emit(percent)
                    else:
                        percent = self.percent_length

                    # 处理图片
                    statistic_dic = {name: 0 for name in names}
                    img = torch.from_numpy(img).to(device)
                    img = img.half() if half else img.float()  # uint8 to fp16/32
                    img /= 255.0  # 0 - 255 to 0.0 - 1.0
                    if img.ndimension() == 3:
                        img = img.unsqueeze(0)
                    # Warmup
                    if device.type != 'cpu' and (
                            old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                        old_img_b = img.shape[0]
                        old_img_h = img.shape[2]
                        old_img_w = img.shape[3]
                        for i in range(3):
                            model(img, augment=augment)[0]

                    # Inference
                    t1 = time_synchronized()
                    with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
                        pred = model(img, augment=augment)[0]
                    t2 = time_synchronized()

                    # Apply NMS
                    pred = non_max_suppression(pred, self.conf, self.iou, classes=classes,
                                               agnostic=agnostic_nms)
                    t3 = time_synchronized()
                    # Process detections
                    for i, det in enumerate(pred):  # detections per image
                        if self.source.isnumeric():
                            p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
                        else:
                            p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)
                        p = Path(p)  # to Path
                        csvname = p.name.split('.')[0]
                        # if(self.source.isnumeric()==False):
                        self.save_path = str(save_dir / p.name)  # img.jpg
                        self.txt_path = str(save_dir / 'labels' / p.stem) + (
                            '' if dataset.mode == 'image' else f'_{frame}')  # img.txt

                        # 新增（创建txt文件）
                        if not tracing:
                            location_txt_dir = str(save_dir) + '/location'
                            if not os.path.exists(location_txt_dir):
                                os.makedirs(location_txt_dir)
                            location_txt_path = location_txt_dir + '\\' + str(p.stem) + (
                            '' if dataset.mode == 'image' else f'_{frame}')  # location_center.txt
                            # print(location_txt_path)
                            flocation = open(location_txt_path + '.txt', 'a')  # 保存检测框中点
                            # print(save_dir)
                        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                        if len(det):
                            # Rescale boxes from img_size to im0 size
                            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                            #新增
                            # Print results
                            for c in det[:, -1].unique():
                                n = (det[:, -1] == c).sum()  # detections per class
                                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                           #

                            # ..................USE TRACK FUNCTION....................
                            # pass an empty array to sort
                            if tracing:
                                dets_to_sort = np.empty((0, 6))

                                # NOTE: We send in detected object class too
                                for x1, y1, x2, y2, conf, detclass in det.cpu().detach().numpy():
                                    dets_to_sort = np.vstack((dets_to_sort,
                                                              np.array([x1, y1, x2, y2, conf, detclass])))

                                # Run SORT
                                tracked_dets = sort_tracker.update(dets_to_sort)
                                tracks = sort_tracker.getTrackers()

                                txt_str = ""

                                # loop over tracks
                                for track in tracks:
                                    # color = compute_color_for_labels(id)
                                    # draw colored tracks
                                    if colored_trk:
                                        [cv2.line(im0, (int(track.centroidarr[i][0]),
                                                        int(track.centroidarr[i][1])),
                                                  (int(track.centroidarr[i + 1][0]),
                                                   int(track.centroidarr[i + 1][1])),
                                                  rand_color_list[track.id], thickness=2)
                                         for i, _ in enumerate(track.centroidarr)
                                         if i < len(track.centroidarr) - 1]
                                        # draw same color tracks
                                    else:
                                        [cv2.line(im0, (int(track.centroidarr[i][0]),
                                                        int(track.centroidarr[i][1])),
                                                  (int(track.centroidarr[i + 1][0]),
                                                   int(track.centroidarr[i + 1][1])),
                                                  (255, 0, 0), thickness=2)
                                         for i, _ in enumerate(track.centroidarr)
                                         if i < len(track.centroidarr) - 1]

                                    if save_txt and not save_with_object_id:
                                        # Normalize coordinates
                                        txt_str += "%i %i %f %f" % (
                                        track.id, track.detclass, track.centroidarr[-1][0] / im0.shape[1],
                                        track.centroidarr[-1][1] / im0.shape[0])
                                        if save_bbox_dim:
                                            txt_str += " %f %f" % (
                                            np.abs(track.bbox_history[-1][0] - track.bbox_history[-1][2]) / im0.shape[0],
                                            np.abs(track.bbox_history[-1][1] - track.bbox_history[-1][3]) / im0.shape[1])
                                        txt_str += "\n"

                                if save_txt and not save_with_object_id:
                                    with open(self.txt_path + '.txt', 'a') as f:
                                        f.write(txt_str)

                                # draw boxes for visualization
                                if len(tracked_dets) > 0:
                                    bbox_xyxy = tracked_dets[:, :4]
                                    identities = tracked_dets[:, 8]
                                    categories = tracked_dets[:, 4]
                                    draw_boxes(im0, bbox_xyxy, identities, categories, names, save_with_object_id, self.txt_path)
                            # ........................................................
                            # Write results
                            else:
                                for *xyxy, conf, cls in reversed(det):
                                    # Add bbox to image
                                    c = int(cls)  # integer class
                                    c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                                    # print("左上点的坐标为：(" + str(c1[0]) + "," + str(c1[1]) + ")，右下点的坐标为(" + str(c2[0]) + "," + str(c2[1]) + ")")
                                    # 新增（获取目标框坐标）
                                    # 左上角
                                    x1 = int(xyxy[0].item())
                                    y1 = int(xyxy[1].item())
                                    # 右下角
                                    x2 = int(xyxy[2].item())
                                    y2 = int(xyxy[3].item())
                                    object_name = names[int(cls)]  # 获取标签名
                                    # if (self.source.isnumeric() == False):
                                    flocation.write(
                                        object_name + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + '\n')
                                    weight = abs(c2[1] - c1[1])
                                    length = abs(c2[0] - c1[0])
                                    diagonal = round(((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2) ** 0.5, 2)
                                    areas = round(abs(c2[1] - c1[1]) * abs(c2[0] - c1[0]), 2)
                                    statistic_dic[names[c]] += 1
                                    label = f'{names[int(cls)]} {conf:.2f}'
                                    color_dict = {'1': [220, 20, 60], '2': [75, 195, 185], '3': [255, 165, 0],
                                                  '4': [60, 20, 220], '5': [228, 228, 37], '6': [68, 228, 37],
                                                  '7': [221, 37, 228], '8': [229, 116, 67]}
                                    if names[int(cls)] == 'Longgitudinal_cracks':
                                        ch_text = '%s,裂缝长度:%s,%.2f' % ('纵向裂缝', diagonal, conf)
                                        color_single = color_dict['1']
                                    elif names[int(cls)] == 'DeepLonggitudinal_cracks':
                                        ch_text = '%s,%.2f' % ('纵向分割线', conf)
                                        color_single = color_dict['2']
                                    elif names[int(cls)] == 'Lateral_cracks':
                                        ch_text = '%s,裂缝长度:%s,%.2f' % ('横向裂缝', diagonal, conf)
                                        color_single = color_dict['3']
                                    elif names[int(cls)] == 'DeepLateral_cracks':
                                        ch_text = '%s,%.2f' % ('横向分割线', conf)
                                        color_single = color_dict['4']
                                    elif names[int(cls)] == 'Alligator_cracks':
                                        ch_text = '%s,龟裂纹面积:%s,%.2f' % ('龟裂', areas, conf)
                                        color_single = color_dict['5']
                                    elif names[int(cls)] == 'Potholes':
                                        ch_text = '%s,坑洼面积:%s,%.2f' % ('坑洼', areas, conf)
                                        color_single = color_dict['6']
                                    elif names[int(cls)] == 'Zebra_crossing':
                                        ch_text = '%s,%.2f' % ('斑马线', conf)
                                        color_single = color_dict['7']
                                    elif names[int(cls)] == 'White_line':
                                        ch_text = '%s,%.2f' % ('白线', conf)
                                        color_single = color_dict['8']
                                    # plot_one_box(xyxy, im0, label=label, color=colors[int(cls]), line_thickness=1)
                                    im0 = plot_one_box(xyxy, im0, label=label, ch_text=ch_text, color=color_single,
                                                       line_thickness=3)
                                    # plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)
                        # if (self.source.isnumeric() == False):
                            if not tracing:
                                flocation.close()
                         # Print time (inference + NMS)
                        print(
                            f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')
                    # Stream results
                    if self.latency!=0:
                        time.sleep(self.latency/600)
                    self.send_output.emit(im0)
                    # print(im0.ctypes)
                    self.send_result.emit(statistic_dic)
                    # Stream results
                    # if view_img:
                    #     cv2.imshow(str(p), im0)
                    #     if cv2.waitKey(1) == ord('q'):  # q to quit
                    #         cv2.destroyAllWindows()
                    #         raise StopIteration
                    # Save results (image with detections)
                    # 截取图片函数（新增）
                    # if (self.source.isnumeric()==False):
                    img_path = str(save_dir).replace('\\', '/')
                    # label_path = str(location_txt_dir).replace('\\', '/')
                    # if(self.source.isnumeric()==False):
                    if save_img:
                        if dataset.mode == 'image':
                            cv2.imwrite(self.save_path, im0)
                            print(f" The image with the result is saved in: {self.save_path}")
                        else:  # 'video' or 'stream'
                            if vid_path != self.save_path:  # new video
                                vid_path = self.save_path
                                if isinstance(self.vid_writer, cv2.VideoWriter):
                                    self.vid_writer.release()  # release previous video writer
                                if self.vid_cap:  # video
                                    fps = self.vid_cap.get(cv2.CAP_PROP_FPS)
                                    w = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                    h = int(self.vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                else:  # stream
                                    fps, w, h = 20, im0.shape[1], im0.shape[0]
                                    self.save_path += '.mp4'
                                self.vid_writer = cv2.VideoWriter(self.save_path,
                                                                      cv2.VideoWriter_fourcc(*'mp4v'),
                                                                      fps,
                                                                      (w, h))
                            self.vid_writer.write(im0)
                    if self.vid_cap or dataset.mode == 'image':
                        if percent == self.percent_length:
                            # print(count)
                            self.send_percent.emit(0)
                            self.send_msg.emit('Finished')
                            if self.vid_writer is not None:
                                self.vid_writer.release()
                            break
            #新增
            # 保存文件夹的路径
            # savepath = 'D:/pycharm/PycharmProjects/yolov7-Pyside6-main/yolov7-Pyside6-main/result'
            # # 将一级目录下的所有文件夹的名称以列表的形式保存
            # dirs = "D:/pycharm/PycharmProjects/yolov7-Pyside6-main/yolov7-Pyside6-main/" + img_path
            # # pp = Path(path)  # to Path
            # dir = img_path.split('/')[1]
            # files = os.listdir(dirs)
            # file_total = []
            # for file in files:
            #     name, type = os.path.splitext(file)
            #     if type == ('.mp4'):
            #         file_total.append(file)
            #         filename = ''.join(str(i) for i in file_total)
            #         # 得到每个视频文件的绝对路径，并利用切分函数对其进行切分，为了防止异常发生，在出现异常的时候可以继续运行该函数
            #         paths = dirs + '/' + filename
            #         print(paths, dir, filename, savepath)
            #         self.video_to_frames(paths, dir, filename, savepath)
            # # 新增函数
            # self.CropImage4File('./' + str(img_path) + '/', './' + str(label_path) + '/',
            #                     './cut')
            if tracing:
                pathl = str(img_path + '/labels')
                print(pathl)
                filelist = os.listdir(pathl)  # 遍历该文件夹下所有的文件（包括文件夹）
                # filelist.sort(key=lambda x:int(x[:-4]))                    #按文件名倒着数第四位开始排序，默认从小到大
                for image_id in filelist:
                    # print(image_id)
                    position = pathl + "\\" + image_id
                    # aa=image_id.strip('.txt')
                    # print(aa)
                    with open(position, "r",encoding='utf-8') as f1, open(str(img_path +'/total.txt'), "a",encoding='utf-8') as f2:
                        strs = f1.readline()
                        # 循环读取
                        while strs:
                            strs1 = strs.split(' ')
                            print(image_id, strs1[0], strs1[1],strs1[2],strs1[3])
                            # print(type(strs1[3]))
                            # if(int(n)<int(str1[0])):
                            #     n=int(str1[0])
                            if strs1[1]=='5':
                                strs1[1]='洼坑'
                                f2.write("%s %s %s %s\n" % (strs1[0], strs1[1],'0',strs1[3]))
                            else:
                                if strs1[1] == '0':
                                    strs1[1] = '纵向裂缝'
                                if strs1[1] == '1':
                                    strs1[1] = '纵向分割线'
                                if strs1[1] == '2':
                                    strs1[1] = '横向裂缝'
                                if strs1[1] == '3':
                                    strs1[1] = '横向分割线'
                                if strs1[1] == '4':
                                    strs1[1] = '龟裂'
                                if strs1[1] == '6':
                                    strs1[1] = '斑马线'
                                if strs1[1] == '7':
                                    strs1[1] = '白线'
                                f2.write("%s %s %s %s\n" % (strs1[0], strs1[1], strs1[2], '0'))
                            strs = f1.readline()
                # print("缺陷总数为{}".format(n))
                print("整理完成")
                # path = r"E:\yolov7-Pyside6-test\result\exp7\total.txt"
                patht = str(img_path + '/total.txt')
                # path1 = r"E:\yolov7-Pyside6-test\result\exp7\total_ok.txt"
                patht1 = str(img_path + '/total_ok.txt')
                # 打开待处理和目标txt文件
                with open(patht, 'r', encoding='utf-8') as f1, \
                        open(patht1, 'w', encoding='utf-8') as f2:
                    # 读取待处理txt文件中的数据
                    lines = f1.readlines()
                    # 遍历待处理数据，去除重复项并写入目标txt文件
                    keywords = set()
                    for line in lines:
                        keyword = line.split(' ')[0]+' '+line.split(' ')[1]  # 获取关键字
                        if keyword not in keywords:
                            f2.write(line)
                            keywords.add(keyword)
                        else:
                            print(f'重复数据已去除：{line}')
                    # 关闭文件
                    f1.close()
                    f2.close()
                #txt转csv
                data_txtDF = pd.read_csv(patht1, sep=' ', header=None, names=['编号', '缺陷类别', '裂缝长度', '洼坑面积'],
                                         dtype={'编号': str, '缺陷类别': str})
                data_txtDF.to_csv(img_path + '/total.csv', index=False, header=['编号', '缺陷类别', '裂缝长度', '洼坑面积'])
                files = open(patht1, "r+",encoding='utf-8')
                # 先读取一行
                strs = files.readline()
                N = 0
                L = []
                # 循环读取
                while strs:
                    strs1 = strs.strip('\n')
                    strs2 = strs1.split(' ')
                    print(strs2[1])
                    L.append(strs2[1])
                    N = N + 1
                    strs = files.readline()
                files.close()
                results = {}
                for i in set(L):
                    results[i] = L.count(i)
                print(results)
                # if '0' in results.keys():
                #     results.update({'纵向裂缝': results.pop("0")})
                # if '1' in results.keys():
                #     results.update({'纵向分割线': results.pop("1")})
                # if '2' in results.keys():
                #     results.update({'横向裂缝': results.pop("2")})
                # if '3' in results.keys():
                #     results.update({'横向分割线': results.pop("3")})
                # if '4' in results.keys():
                #     results.update({'龟裂': results.pop("4")})
                # if '5' in results.keys():
                #     results.update({'洼坑': results.pop("5")})
                # if '6' in results.keys():
                #     results.update({'斑马线': results.pop("6")})
                # if '7' in results.keys():
                #     results.update({'白线': results.pop("7")})
                print("总缺陷{}处".format(N))
                # print(results)
                header = ['缺陷类别', '数量']  # 数据列名
                # print(results.items())
                with open(img_path+'/'+csvname + '.csv', 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    for row in results.items():
                        writer.writerow(row)
            print(f'Done. ({time.time() - start_time:.3f}s)')
        except Exception as e:
            self.send_msg.emit("程序出错啦!!!   " + str(e))
