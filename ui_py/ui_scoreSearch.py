# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'scoreSearch.ui'
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QSizePolicy, QWidget)

class Ui_scoreSearch(object):
    def setupUi(self, scoreSearch):
        if not scoreSearch.objectName():
            scoreSearch.setObjectName(u"scoreSearch")
        scoreSearch.resize(613, 600)
        self.dateEdit = QDateEdit(scoreSearch)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setGeometry(QRect(140, 110, 110, 24))

        self.retranslateUi(scoreSearch)

        QMetaObject.connectSlotsByName(scoreSearch)
    # setupUi

    def retranslateUi(self, scoreSearch):
        scoreSearch.setWindowTitle(QCoreApplication.translate("scoreSearch", u"Form", None))
    # retranslateUi

