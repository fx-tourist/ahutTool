# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLayout, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_mian(object):
    def setupUi(self, mian):
        if not mian.objectName():
            mian.setObjectName(u"mian")
        mian.resize(638, 494)
        self.horizontalLayout = QHBoxLayout(mian)
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 9, 9, 9)
        self.selectTools = QScrollArea(mian)
        self.selectTools.setObjectName(u"selectTools")
        self.selectTools.setMinimumSize(QSize(150, 0))
        self.selectTools.setMaximumSize(QSize(150, 16777215))
        self.selectTools.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 148, 474))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.userInfo_button = QPushButton(self.scrollAreaWidgetContents)
        self.userInfo_button.setObjectName(u"userInfo_button")
        self.userInfo_button.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.userInfo_button)

        self.selfPrint_button = QPushButton(self.scrollAreaWidgetContents)
        self.selfPrint_button.setObjectName(u"selfPrint_button")
        self.selfPrint_button.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.selfPrint_button)

        self.examSearch_button = QPushButton(self.scrollAreaWidgetContents)
        self.examSearch_button.setObjectName(u"examSearch_button")
        self.examSearch_button.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.examSearch_button)

        self.classSchedule_button = QPushButton(self.scrollAreaWidgetContents)
        self.classSchedule_button.setObjectName(u"classSchedule_button")
        self.classSchedule_button.setMinimumSize(QSize(0, 50))

        self.verticalLayout.addWidget(self.classSchedule_button)

        self.robClasses_button = QPushButton(self.scrollAreaWidgetContents)
        self.robClasses_button.setObjectName(u"robClasses_button")
        self.robClasses_button.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.robClasses_button)

        self.settings_button = QPushButton(self.scrollAreaWidgetContents)
        self.settings_button.setObjectName(u"settings_button")
        self.settings_button.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.settings_button)

        self.appInfo_button = QPushButton(self.scrollAreaWidgetContents)
        self.appInfo_button.setObjectName(u"appInfo_button")
        self.appInfo_button.setMinimumSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.appInfo_button)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.selectTools.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.selectTools)

        self.subWidget = QWidget(mian)
        self.subWidget.setObjectName(u"subWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subWidget.sizePolicy().hasHeightForWidth())
        self.subWidget.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.subWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.subWidgetLayout = QVBoxLayout()
        self.subWidgetLayout.setSpacing(0)
        self.subWidgetLayout.setObjectName(u"subWidgetLayout")
        self.subWidgetLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        self.verticalLayout_3.addLayout(self.subWidgetLayout)


        self.horizontalLayout.addWidget(self.subWidget)


        self.retranslateUi(mian)

        QMetaObject.connectSlotsByName(mian)
    # setupUi

    def retranslateUi(self, mian):
        mian.setWindowTitle(QCoreApplication.translate("mian", u"mian", None))
        self.userInfo_button.setText(QCoreApplication.translate("mian", u"\u8d26\u53f7", None))
        self.selfPrint_button.setText(QCoreApplication.translate("mian", u"\u81ea\u52a9\u6253\u5370", None))
        self.examSearch_button.setText(QCoreApplication.translate("mian", u"\u8003\u8bd5\u67e5\u8be2", None))
        self.classSchedule_button.setText(QCoreApplication.translate("mian", u"\u8bfe\u7a0b\u8868", None))
        self.robClasses_button.setText(QCoreApplication.translate("mian", u"\u62a2\u8bfe\u52a9\u624b", None))
        self.settings_button.setText(QCoreApplication.translate("mian", u"\u8bbe\u7f6e", None))
        self.appInfo_button.setText(QCoreApplication.translate("mian", u"\u5173\u4e8e", None))
    # retranslateUi

