# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)
import app_rc
import apprcc_rc

class Login_Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(500, 300)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(500, 300))
        Form.setMaximumSize(QSize(500, 300))
        icon = QIcon()
        icon.addFile(u":/img/img/icons/swimming.png", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet(u"background-color: rgb(249, 249, 249);")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 221, 51))
        self.label.setStyleSheet(u"border-image: url(:/img/Settings/main_window_img/school_logo.jpg);")
        self.label.setPixmap(QPixmap(u"images/small_log.png"))
        self.title = QLabel(Form)
        self.title.setObjectName(u"title")
        self.title.setGeometry(QRect(50, 60, 421, 61))
        font = QFont()
        font.setFamilies([u"Times New Roman"])
        font.setPointSize(20)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.edit_username = QLineEdit(Form)
        self.edit_username.setObjectName(u"edit_username")
        self.edit_username.setGeometry(QRect(180, 130, 113, 20))
        self.edit_password = QLineEdit(Form)
        self.edit_password.setObjectName(u"edit_password")
        self.edit_password.setGeometry(QRect(180, 180, 113, 20))
        self.btn_login = QPushButton(Form)
        self.btn_login.setObjectName(u"btn_login")
        self.btn_login.setGeometry(QRect(200, 220, 75, 23))
        self.btn_regeist = QPushButton(Form)
        self.btn_regeist.setObjectName(u"btn_regeist")
        self.btn_regeist.setGeometry(QRect(410, 260, 75, 23))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u82cf\u7eb3\u5b87-\u57fa\u4e8e\u6df1\u5ea6\u5b66\u4e60\u7684\u8def\u9762\u88c2\u7f1d\u68c0\u6d4b\u7cfb\u7edf", None))
        self.label.setText("")
        self.title.setText(QCoreApplication.translate("Form", u"\u6b22\u8fce\u767b\u5f55\u8def\u9762\u88c2\u7f1d\u68c0\u6d4b\u7cfb\u7edf", None))
        self.edit_username.setPlaceholderText(QCoreApplication.translate("Form", u"\u7528\u6237\u540d", None))
        self.edit_password.setPlaceholderText(QCoreApplication.translate("Form", u"\u5bc6\u7801", None))
        self.btn_login.setText(QCoreApplication.translate("Form", u"\u767b\u5f55", None))
        self.btn_regeist.setText(QCoreApplication.translate("Form", u"\u6ce8\u518c", None))
    # retranslateUi

