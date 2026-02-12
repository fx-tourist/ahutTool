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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_userInfo(object):
    def setupUi(self, userInfo):
        if not userInfo.objectName():
            userInfo.setObjectName(u"userInfo")
        userInfo.resize(600, 454)
        self.gridLayout = QGridLayout(userInfo)
        self.gridLayout.setObjectName(u"gridLayout")
        self.userIdTxt = QLabel(userInfo)
        self.userIdTxt.setObjectName(u"userIdTxt")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userIdTxt.sizePolicy().hasHeightForWidth())
        self.userIdTxt.setSizePolicy(sizePolicy)
        self.userIdTxt.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.userIdTxt, 3, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.classTxt = QLabel(userInfo)
        self.classTxt.setObjectName(u"classTxt")
        sizePolicy.setHeightForWidth(self.classTxt.sizePolicy().hasHeightForWidth())
        self.classTxt.setSizePolicy(sizePolicy)
        self.classTxt.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.classTxt, 6, 1, 1, 1)

        self.userMajor = QLabel(userInfo)
        self.userMajor.setObjectName(u"userMajor")
        sizePolicy.setHeightForWidth(self.userMajor.sizePolicy().hasHeightForWidth())
        self.userMajor.setSizePolicy(sizePolicy)
        self.userMajor.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.userMajor, 5, 2, 1, 1)

        self.userDepartment = QLabel(userInfo)
        self.userDepartment.setObjectName(u"userDepartment")
        sizePolicy.setHeightForWidth(self.userDepartment.sizePolicy().hasHeightForWidth())
        self.userDepartment.setSizePolicy(sizePolicy)
        self.userDepartment.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.userDepartment, 4, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 8, 2, 1, 1)

        self.userClass = QLabel(userInfo)
        self.userClass.setObjectName(u"userClass")
        sizePolicy.setHeightForWidth(self.userClass.sizePolicy().hasHeightForWidth())
        self.userClass.setSizePolicy(sizePolicy)
        self.userClass.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.userClass, 6, 2, 1, 1)

        self.userNameTxt = QLabel(userInfo)
        self.userNameTxt.setObjectName(u"userNameTxt")
        sizePolicy.setHeightForWidth(self.userNameTxt.sizePolicy().hasHeightForWidth())
        self.userNameTxt.setSizePolicy(sizePolicy)
        self.userNameTxt.setMaximumSize(QSize(120, 16777215))
        self.userNameTxt.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.userNameTxt, 2, 1, 1, 1)

        self.yuanxiTxt = QLabel(userInfo)
        self.yuanxiTxt.setObjectName(u"yuanxiTxt")
        sizePolicy.setHeightForWidth(self.yuanxiTxt.sizePolicy().hasHeightForWidth())
        self.yuanxiTxt.setSizePolicy(sizePolicy)
        self.yuanxiTxt.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.yuanxiTxt, 4, 1, 1, 1)

        self.userName = QLabel(userInfo)
        self.userName.setObjectName(u"userName")
        sizePolicy.setHeightForWidth(self.userName.sizePolicy().hasHeightForWidth())
        self.userName.setSizePolicy(sizePolicy)
        self.userName.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.userName, 2, 2, 1, 1)

        self.messageShow = QLabel(userInfo)
        self.messageShow.setObjectName(u"messageShow")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.messageShow.sizePolicy().hasHeightForWidth())
        self.messageShow.setSizePolicy(sizePolicy1)
        self.messageShow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.messageShow, 7, 1, 1, 2)

        self.loginOut_button = QPushButton(userInfo)
        self.loginOut_button.setObjectName(u"loginOut_button")

        self.gridLayout.addWidget(self.loginOut_button, 10, 2, 1, 1)

        self.major = QLabel(userInfo)
        self.major.setObjectName(u"major")
        sizePolicy.setHeightForWidth(self.major.sizePolicy().hasHeightForWidth())
        self.major.setSizePolicy(sizePolicy)
        self.major.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.major, 5, 1, 1, 1)

        self.userId = QLabel(userInfo)
        self.userId.setObjectName(u"userId")
        sizePolicy.setHeightForWidth(self.userId.sizePolicy().hasHeightForWidth())
        self.userId.setSizePolicy(sizePolicy)
        self.userId.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.userId, 3, 2, 1, 1)

        self.userAvatar = QLabel(userInfo)
        self.userAvatar.setObjectName(u"userAvatar")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.userAvatar.sizePolicy().hasHeightForWidth())
        self.userAvatar.setSizePolicy(sizePolicy2)
        self.userAvatar.setMinimumSize(QSize(100, 100))

        self.gridLayout.addWidget(self.userAvatar, 0, 1, 2, 2)


        self.retranslateUi(userInfo)

        QMetaObject.connectSlotsByName(userInfo)
    # setupUi

    def retranslateUi(self, userInfo):
        userInfo.setWindowTitle(QCoreApplication.translate("userInfo", u"Form", None))
        self.userIdTxt.setText(QCoreApplication.translate("userInfo", u"\u5b66\u53f7:", None))
        self.classTxt.setText(QCoreApplication.translate("userInfo", u"\u73ed\u7ea7:", None))
        self.userMajor.setText(QCoreApplication.translate("userInfo", u"userMajor", None))
        self.userDepartment.setText(QCoreApplication.translate("userInfo", u"userDepartment", None))
        self.userClass.setText(QCoreApplication.translate("userInfo", u"userClass", None))
        self.userNameTxt.setText(QCoreApplication.translate("userInfo", u"\u59d3\u540d:", None))
        self.yuanxiTxt.setText(QCoreApplication.translate("userInfo", u"\u9662\u7cfb:", None))
        self.userName.setText(QCoreApplication.translate("userInfo", u"userName", None))
        self.messageShow.setText("")
        self.loginOut_button.setText(QCoreApplication.translate("userInfo", u"\u9000\u51fa\u767b\u5f55", None))
        self.major.setText(QCoreApplication.translate("userInfo", u"\u4e13\u4e1a:", None))
        self.userId.setText(QCoreApplication.translate("userInfo", u"userId", None))
        self.userAvatar.setText("")
    # retranslateUi

