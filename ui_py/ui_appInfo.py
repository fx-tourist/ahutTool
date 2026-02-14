# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'appInfo.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_appInfo(object):
    def setupUi(self, appInfo):
        if not appInfo.objectName():
            appInfo.setObjectName(u"appInfo")
        appInfo.resize(633, 541)
        self.gridLayout = QGridLayout(appInfo)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.icon = QLabel(appInfo)
        self.icon.setObjectName(u"icon")
        self.icon.setMaximumSize(QSize(256, 256))
        self.icon.setSizeIncrement(QSize(20, 0))
        self.icon.setScaledContents(True)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon.setWordWrap(True)

        self.gridLayout.addWidget(self.icon, 0, 0, 1, 1)

        self.label_2 = QLabel(appInfo)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setWordWrap(True)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)


        self.retranslateUi(appInfo)

        QMetaObject.connectSlotsByName(appInfo)
    # setupUi

    def retranslateUi(self, appInfo):
        appInfo.setWindowTitle(QCoreApplication.translate("appInfo", u"appInfo", None))
        self.icon.setText("")
        self.label_2.setText(QCoreApplication.translate("appInfo", u"<html><head/><body><p>\u8f6f\u4ef6\u4f5c\u8005:fx_tourist</p><p>\u56fe\u6807\u6765\u6e90\uff1aiconfont</p><p>\u56fe\u6807\u4f5c\u8005\uff1ahnck2000</p><p>\u56fe\u7247\u6765\u6e90\u5747\u4e3a\u5b89\u5de5\u5927\u5b98\u7f51</p><p>\u672c\u8f6f\u4ef6\u4f7f\u7528 Qt \u6846\u67b6 \u5f00\u53d1\u3002</p><p>Qt \u7531 The Qt Company \u5f00\u53d1\uff0c\u57fa\u4e8e LGPLv3 \u5f00\u6e90\u534f\u8bae\u6388\u6743\u3002</p><p>Qt \u7248\u6743\u6240\u6709 \u00a9 The Qt Company Ltd. \u4fdd\u7559\u6240\u6709\u6743\u5229\u3002</p></body></html>", None))
    # retranslateUi

