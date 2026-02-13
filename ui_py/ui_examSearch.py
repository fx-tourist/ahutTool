# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'examSearch.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QLabel,
    QSizePolicy, QTableView, QVBoxLayout, QWidget)

class Ui_examSearch(object):
    def setupUi(self, examSearch):
        if not examSearch.objectName():
            examSearch.setObjectName(u"examSearch")
        examSearch.resize(533, 500)
        self.verticalLayout = QVBoxLayout(examSearch)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.examTable1 = QTableView(examSearch)
        self.examTable1.setObjectName(u"examTable1")
        self.examTable1.setStyleSheet(u"QTableView{border:none;}")
        self.examTable1.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.verticalLayout.addWidget(self.examTable1)

        self.messageShow1 = QLabel(examSearch)
        self.messageShow1.setObjectName(u"messageShow1")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageShow1.sizePolicy().hasHeightForWidth())
        self.messageShow1.setSizePolicy(sizePolicy)
        self.messageShow1.setWordWrap(True)
        self.messageShow1.setIndent(-2)

        self.verticalLayout.addWidget(self.messageShow1)

        self.examTable2 = QTableView(examSearch)
        self.examTable2.setObjectName(u"examTable2")
        self.examTable2.setStyleSheet(u"QTableView{border:none;}")
        self.examTable2.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.verticalLayout.addWidget(self.examTable2)

        self.messageShow = QLabel(examSearch)
        self.messageShow.setObjectName(u"messageShow")
        sizePolicy.setHeightForWidth(self.messageShow.sizePolicy().hasHeightForWidth())
        self.messageShow.setSizePolicy(sizePolicy)
        self.messageShow.setWordWrap(True)

        self.verticalLayout.addWidget(self.messageShow)


        self.retranslateUi(examSearch)

        QMetaObject.connectSlotsByName(examSearch)
    # setupUi

    def retranslateUi(self, examSearch):
        examSearch.setWindowTitle(QCoreApplication.translate("examSearch", u"Form", None))
        self.messageShow1.setText("")
        self.messageShow.setText("")
    # retranslateUi

