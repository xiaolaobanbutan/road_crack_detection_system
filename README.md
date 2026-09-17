# Road Crack Detection System / 路面裂缝检测系统

基于深度学习的路面病害检测桌面原型。项目将图像标注、模型训练、目标检测、图像分类和裂缝分割整合到 PySide6 界面中，支持图片、视频及摄像头输入。检测模块使用 YOLOv7 风格的代码，分类模块使用 PyTorch，分割模块使用 U-Net。项目主要用于课程设计与功能展示；代码中的模型和工具含有第三方实现，详见 [来源与许可](#来源与许可)。

## 功能与代码结构

| 功能 | 主要文件 | 说明 |
| --- | --- | --- |
| 检测与跟踪 | `YoloClass.py`, `models/`, `utils/`, `sort.py` | 检测框、类别、轨迹显示；可选择本地 `.pt` 权重。 |
| 裂缝分类 | `pytorchClass.py` | 对图像或视频帧进行病害类别识别；类别映射见 `idx_to_labels*.npy`。 |
| 裂缝分割 | `crack_segclass.py`, `Model/` | U-Net 单通道裂缝掩膜预测。 |
| 标注与训练 | `labelImg.py`, `libs/`, `Train_Ui.py` | 图像框选标注、训练参数界面及实验性训练代码。 |
| 界面 | `main.py`, `main_login.py`, `recognizition.py`, `ui/` | 检测界面与完整导航界面。 |

## 环境与启动

建议在 Python 3.8–3.10 的独立虚拟环境中运行。本仓库未包含 CUDA、PyTorch 和 torchvision 的安装包，请先按自己的设备安装相互匹配的版本；旧代码使用 `mmcv` 1.x API。然后在仓库根目录执行：

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install torch torchvision
python -m pip install -r requirements.txt
python main.py                      # 直接打开检测界面
```

完整导航界面可用 `python main_login.py` 启动，首次使用需注册本地演示账号。账号数据写入未跟踪的 `userInfo.csv`，密码以 PBKDF2 哈希保存；该登录仅用于本地演示，不提供在线用户服务。

运行命令请在**仓库根目录**执行。`ptmodel/`、`checkpoint/` 和 `umodel/` 分别用于检测、分类和分割权重。仓库只保留空目录标记；需要自行放入与代码结构匹配且有权使用的权重。示例默认路径如下：

```text
ptmodel/yolov7.pt                  # YOLOv7 检测权重，可在界面中切换其他 .pt
checkpoint/best6-0.839.pth        # PyTorch 分类权重，可在界面中切换其他 .pth
umodel/best_model_2.pth           # U-Net 分割权重
```

上面的权重文件名仅反映原项目配置，**仓库没有提供权重下载地址，也不保证通用预训练权重可直接识别路面病害**。分类权重的类别顺序需与 `idx_to_labels*.npy` 一致。缺少相应权重时可浏览界面，但不能完成对应推理。

## 使用流程

1. 准备路面图像、视频或摄像头，以及对应模型权重。
2. 用 `python main.py` 打开检测界面；选择输入源和模型，设置信心阈值与 IoU 阈值后开始检测。
3. 切换到分类或分割功能时，分别检查 `checkpoint/` 和 `umodel/` 中的权重。
4. 如需使用标注和训练入口，运行 `python main_login.py`。U-Net 训练数据加载器要求 `Training_Images/*.jpg` 与 `Training_Labels/*.png` 按同名配对；训练代码属于原型，需要根据自己的数据与环境进一步调整。

## 发布范围与验证状态

公开版本移除了 IDE 配置、虚拟环境、重复权重、个人账号 CSV、原始数据、输出视频及缓存，原目录保持不变。修正了检测界面的固定 Windows UI 路径和字体路径，并使本地账号文件在首次启动时可自动创建。依赖清单根据源码实际导入整理，取代原来的机器环境导出文件。

已完成 Python 源码语法检查和本地账号读写检查。本次整理环境没有安装 PySide6、PyTorch、torchvision、mmcv 等全部依赖，也没有合适的公开模型权重与数据集，因此**尚未完成完整 GUI 启动、模型推理或指标复现**。原文件名中的准确率数字不能视为本仓库验证结果。

## 来源与许可

这是课程项目的集成与界面开发版本，不将基础模型和标注工具声称为原创。主要参考及复用部分：

- [YOLOv7](https://github.com/WongKinYiu/yolov7)：检测模型及相关 `models/`、`utils/` 实现，GPL-3.0。
- [PyTorch-UNet](https://github.com/milesial/Pytorch-UNet)：`Model/` 中 U-Net 结构的参考实现，GPL-3.0。
- [SORT](https://github.com/abewley/sort)：`sort.py` 跟踪算法的参考实现，GPL。
- [labelImg](https://github.com/HumanSignal/labelImg)：`labelImg.py` 与 `libs/` 标注工具的参考实现，MIT。

由于包含 GPL-3.0 代码，本仓库按 [GPL-3.0](LICENSE) 发布；labelImg 的 MIT 版权与许可声明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。字体 `Font/FiraMono-Medium.otf` 的 OFL 声明保留在 `Font/SIL Open Font License.txt`。
