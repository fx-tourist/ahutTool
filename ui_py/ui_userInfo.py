# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'userInfo.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_userInfo(object):
    def setupUi(self, userInfo):
        if not userInfo.objectName():
            userInfo.setObjectName(u"userInfo")
        userInfo.resize(600, 454)
        self.gridLayout = QGridLayout(userInfo)
        self.gridLayout.setObjectName(u"gridLayout")
        self.userNameTxt = QLabel(userInfo)
        self.userNameTxt.setObjectName(u"userNameTxt")
        self.userNameTxt.setMaximumSize(QSize(120, 16777215))
        self.userNameTxt.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.userNameTxt, 3, 1, 1, 1)

        self.userAvatar = QFrame(userInfo)
        self.userAvatar.setObjectName(u"userAvatar")
        self.userAvatar.setMinimumSize(QSize(50, 50))
        self.userAvatar.setMaximumSize(QSize(50, 50))
        self.userAvatar.setFrameShape(QFrame.Shape.StyledPanel)
        self.userAvatar.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.userAvatar, 1, 2, 1, 1)

        self.userId = QLabel(userInfo)
        self.userId.setObjectName(u"userId")

        self.gridLayout.addWidget(self.userId, 4, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 2, 1, 1)

        self.userName = QLabel(userInfo)
        self.userName.setObjectName(u"userName")

        self.gridLayout.addWidget(self.userName, 3, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 3, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 3, 1, 1)

        self.userIdTxt = QLabel(userInfo)
        self.userIdTxt.setObjectName(u"userIdTxt")

        self.gridLayout.addWidget(self.userIdTxt, 4, 1, 1, 1)

        self.exitUser_button = QPushButton(userInfo)
        self.exitUser_button.setObjectName(u"exitUser_button")

        self.gridLayout.addWidget(self.exitUser_button, 7, 2, 1, 1)


        self.retranslateUi(userInfo)

        QMetaObject.connectSlotsByName(userInfo)
    # setupUi

    def retranslateUi(self, userInfo):
        userInfo.setWindowTitle(QCoreApplication.translate("userInfo", u"Form", None))
        self.userNameTxt.setText(QCoreApplication.translate("userInfo", u"\u59d3\u540d:", None))
        self.userId.setText(QCoreApplication.translate("userInfo", u"userId", None))
        self.userName.setText(QCoreApplication.translate("userInfo", u"userName", None))
        self.userIdTxt.setText(QCoreApplication.translate("userInfo", u"\u5b66\u53f7:", None))
        self.exitUser_button.setText(QCoreApplication.translate("userInfo", u"\u9000\u51fa\u767b\u5f55", None))
    # retranslateUi

