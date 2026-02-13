# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'selfPrint.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QScrollArea, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_selfPrint(object):
    def setupUi(self, selfPrint):
        if not selfPrint.objectName():
            selfPrint.setObjectName(u"selfPrint")
        selfPrint.resize(485, 578)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(selfPrint.sizePolicy().hasHeightForWidth())
        selfPrint.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(selfPrint)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.printListArea = QScrollArea(selfPrint)
        self.printListArea.setObjectName(u"printListArea")
        self.printListArea.setStyleSheet(u"QScrollArea { border: none; }")
        self.printListArea.setWidgetResizable(True)
        self.printListWidget = QWidget()
        self.printListWidget.setObjectName(u"printListWidget")
        self.printListWidget.setGeometry(QRect(0, 0, 485, 563))
        sizePolicy.setHeightForWidth(self.printListWidget.sizePolicy().hasHeightForWidth())
        self.printListWidget.setSizePolicy(sizePolicy)
        self.printListWidget.setStyleSheet(u"QScrollArea {}")
        self.verticalLayout_3 = QVBoxLayout(self.printListWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.selfPrintListLayout = QVBoxLayout()
        self.selfPrintListLayout.setSpacing(0)
        self.selfPrintListLayout.setObjectName(u"selfPrintListLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.selfPrintListLayout.addItem(self.verticalSpacer)


        self.verticalLayout_3.addLayout(self.selfPrintListLayout)

        self.printListArea.setWidget(self.printListWidget)

        self.verticalLayout.addWidget(self.printListArea)

        self.messageShow = QLabel(selfPrint)
        self.messageShow.setObjectName(u"messageShow")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.messageShow.sizePolicy().hasHeightForWidth())
        self.messageShow.setSizePolicy(sizePolicy1)
        self.messageShow.setWordWrap(True)
        self.messageShow.setOpenExternalLinks(False)

        self.verticalLayout.addWidget(self.messageShow)


        self.retranslateUi(selfPrint)

        QMetaObject.connectSlotsByName(selfPrint)
    # setupUi

    def retranslateUi(self, selfPrint):
        selfPrint.setWindowTitle(QCoreApplication.translate("selfPrint", u"Form", None))
        self.messageShow.setText("")
    # retranslateUi

