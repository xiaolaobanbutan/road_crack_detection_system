# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'First_Ui.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import app_rc
import apprcc_rc

class MyWindow_First(object):
    def setupUi(self, MainWindow):
        self.Form = MainWindow
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(977, 650)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setContextMenuPolicy(Qt.NoContextMenu)
        icon = QIcon()
        icon.addFile(u":/img/img/icons/swimming.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"border-image: url(:/img/Settings/main_window_img/background1x.png);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(800, 0))
        self.centralwidget.setMouseTracking(False)
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)

        self.name_label = QLabel(self.centralwidget)
        self.name_label.setObjectName(u"name_label")
        font = QFont()
        font.setFamilies([u"\u9ed1\u4f53"])
        font.setPointSize(28)
        font.setBold(False)
        self.name_label.setFont(font)
        self.name_label.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"\n"
"")

        self.horizontalLayout_2.addWidget(self.name_label)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.model_train = QPushButton(self.centralwidget)
        self.model_train.setObjectName(u"model_train")
        self.model_train.setMinimumSize(QSize(265, 265))
        self.model_train.setStyleSheet(u"QPushButton#model_train{border-image: url(:/img/Settings/main_window_img/train_B.png);}\n"
"\n"
"QPushButton#model_train::hover{\n"
"border-image: url(:/img/Settings/main_window_img/train_A.png);\n"
"}\n"
"\n"
"")
        self.model_train.setIconSize(QSize(50, 50))

        self.horizontalLayout.addWidget(self.model_train)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.accurate_detecte = QPushButton(self.centralwidget)
        self.accurate_detecte.setObjectName(u"accurate_detecte")
        self.accurate_detecte.setMinimumSize(QSize(265, 265))
        self.accurate_detecte.setStyleSheet(u"QPushButton#accurate_detecte{border-image: url(:/img/Settings/main_window_img/detect_B.png);}\n"
"\n"
"QPushButton#accurate_detecte::hover{\n"
"border-image: url(:/img/Settings/main_window_img/detect_A.png);\n"
"}\n"
"")
        self.accurate_detecte.setIconSize(QSize(50, 50))

        self.horizontalLayout.addWidget(self.accurate_detecte)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.data_annno = QPushButton(self.centralwidget)
        self.data_annno.setObjectName(u"data_annno")
        self.data_annno.setMinimumSize(QSize(265, 265))
        self.data_annno.setBaseSize(QSize(14, 14))
        self.data_annno.setStyleSheet(u"QPushButton#data_annno{border-image: url(:/img/Settings/main_window_img/annotation_B.png);}\n"
"\n"
"QPushButton#data_annno::hover{\n"
"border-image: url(:/img/Settings/main_window_img/annotation_A.png);\n"
"}\n"
"\n"
"")

        self.horizontalLayout.addWidget(self.data_annno)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u82cf\u7eb3\u5b87-\u57fa\u4e8e\u6df1\u5ea6\u5b66\u4e60\u7684\u8def\u9762\u88c2\u7f1d\u68c0\u6d4b\u7cfb\u7edf", None))
        self.name_label.setText(QCoreApplication.translate("MainWindow", u"\u8def\u9762\u88c2\u7f1d\u68c0\u6d4b\u7cfb\u7edf", None))
        self.model_train.setText("")
        self.accurate_detecte.setText("")
        self.data_annno.setText("")
    # retranslateUi

