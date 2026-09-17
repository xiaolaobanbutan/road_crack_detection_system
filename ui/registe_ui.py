# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'registe_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)
import app_rc
import apprcc_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        icon = QIcon()
        icon.addFile(u":/img/img/icons/swimming.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet(u"background-color: rgb(249, 249, 249);")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 60, 191, 61))
        font = QFont()
        font.setFamilies([u"Adobe Devanagari"])
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 0, 191, 51))
        self.label_4.setStyleSheet(u"border-image: url(:/img/Settings/main_window_img/school_logo.jpg);")
        self.label_4.setPixmap(QPixmap(u"images/small_log.png"))
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(100, 130, 181, 26))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.edit_username = QLineEdit(self.layoutWidget)
        self.edit_username.setObjectName(u"edit_username")

        self.horizontalLayout.addWidget(self.edit_username)

        self.layoutWidget1 = QWidget(Dialog)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(100, 180, 181, 26))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.edit_password = QLineEdit(self.layoutWidget1)
        self.edit_password.setObjectName(u"edit_password")

        self.horizontalLayout_2.addWidget(self.edit_password)

        self.layoutWidget2 = QWidget(Dialog)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(200, 250, 195, 30))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_regiser = QPushButton(self.layoutWidget2)
        self.pushButton_regiser.setObjectName(u"pushButton_regiser")

        self.horizontalLayout_3.addWidget(self.pushButton_regiser)

        self.pushButton_cancer = QPushButton(self.layoutWidget2)
        self.pushButton_cancer.setObjectName(u"pushButton_cancer")

        self.horizontalLayout_3.addWidget(self.pushButton_cancer)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u8d26\u53f7\u6ce8\u518c", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u8d26\u53f7\u6ce8\u518c", None))
        self.label_4.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u7528\u6237\u540d", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u5bc6  \u7801", None))
        self.pushButton_regiser.setText(QCoreApplication.translate("Dialog", u"\u6ce8\u518c", None))
        self.pushButton_cancer.setText(QCoreApplication.translate("Dialog", u"\u53d6\u6d88", None))
    # retranslateUi

