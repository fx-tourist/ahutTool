# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'classSchedule.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDateEdit,
    QGridLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QWidget)

class Ui_classSchedule(object):
    def setupUi(self, classSchedule):
        if not classSchedule.objectName():
            classSchedule.setObjectName(u"classSchedule")
        classSchedule.resize(657, 586)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(classSchedule.sizePolicy().hasHeightForWidth())
        classSchedule.setSizePolicy(sizePolicy)
        classSchedule.setStyleSheet(u"")
        self.gridLayout = QGridLayout(classSchedule)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.search = QPushButton(classSchedule)
        self.search.setObjectName(u"search")

        self.gridLayout.addWidget(self.search, 2, 4, 1, 1)

        self.classScheduleTable = QTableView(classSchedule)
        self.classScheduleTable.setObjectName(u"classScheduleTable")
        self.classScheduleTable.setStyleSheet(u"QtableWidget{border:none;}")
        self.classScheduleTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.classScheduleTable.horizontalHeader().setMinimumSectionSize(150)
        self.classScheduleTable.horizontalHeader().setDefaultSectionSize(150)
        self.classScheduleTable.verticalHeader().setVisible(False)
        self.classScheduleTable.verticalHeader().setMinimumSectionSize(100)
        self.classScheduleTable.verticalHeader().setDefaultSectionSize(100)

        self.gridLayout.addWidget(self.classScheduleTable, 3, 1, 1, 6)

        self.selectedDate = QLabel(classSchedule)
        self.selectedDate.setObjectName(u"selectedDate")

        self.gridLayout.addWidget(self.selectedDate, 2, 1, 1, 1)

        self.messageShow = QLabel(classSchedule)
        self.messageShow.setObjectName(u"messageShow")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.messageShow.sizePolicy().hasHeightForWidth())
        self.messageShow.setSizePolicy(sizePolicy1)
        self.messageShow.setWordWrap(True)

        self.gridLayout.addWidget(self.messageShow, 4, 1, 1, 6)

        self.dateEdit = QDateEdit(classSchedule)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setTimeSpec(Qt.TimeSpec.LocalTime)

        self.gridLayout.addWidget(self.dateEdit, 2, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 6, 1, 1)

        self.showDetail = QCheckBox(classSchedule)
        self.showDetail.setObjectName(u"showDetail")

        self.gridLayout.addWidget(self.showDetail, 2, 3, 1, 1)


        self.retranslateUi(classSchedule)

        QMetaObject.connectSlotsByName(classSchedule)
    # setupUi

    def retranslateUi(self, classSchedule):
        classSchedule.setWindowTitle(QCoreApplication.translate("classSchedule", u"Form", None))
        self.search.setText(QCoreApplication.translate("classSchedule", u"\u67e5\u8be2", None))
        self.selectedDate.setText(QCoreApplication.translate("classSchedule", u"\u9009\u62e9\u7684\u65e5\u671f", None))
        self.messageShow.setText("")
        self.dateEdit.setDisplayFormat(QCoreApplication.translate("classSchedule", u"yyyy/M/d", None))
        self.showDetail.setText(QCoreApplication.translate("classSchedule", u"\u663e\u793a\u8be6\u7ec6\u8bfe\u8868", None))
    # retranslateUi

