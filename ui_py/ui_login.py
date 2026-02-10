# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTextEdit, QWidget)

class Ui_login(object):
    def setupUi(self, login):
        if not login.objectName():
            login.setObjectName(u"login")
        login.resize(585, 479)
        self.gridLayout = QGridLayout(login)
        self.gridLayout.setObjectName(u"gridLayout")
        self.login_pwd = QLabel(login)
        self.login_pwd.setObjectName(u"login_pwd")
        self.login_pwd.setMaximumSize(QSize(150, 30))
        self.login_pwd.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.login_pwd, 2, 1, 1, 1)

        self.login_id = QLabel(login)
        self.login_id.setObjectName(u"login_id")
        self.login_id.setMaximumSize(QSize(150, 30))
        self.login_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.login_id, 1, 1, 1, 1)

        self.login_message = QLabel(login)
        self.login_message.setObjectName(u"login_message")
        self.login_message.setSizeIncrement(QSize(0, 30))
        self.login_message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.login_message, 4, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.login_button = QPushButton(login)
        self.login_button.setObjectName(u"login_button")

        self.gridLayout.addWidget(self.login_button, 5, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.login_idInput = QTextEdit(login)
        self.login_idInput.setObjectName(u"login_idInput")
        self.login_idInput.setMaximumSize(QSize(300, 30))

        self.gridLayout.addWidget(self.login_idInput, 1, 2, 1, 1)

        self.login_accept = QCheckBox(login)
        self.login_accept.setObjectName(u"login_accept")

        self.gridLayout.addWidget(self.login_accept, 3, 2, 1, 1)

        self.frame = QFrame(login)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 150))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout.addWidget(self.frame, 0, 2, 1, 1)

        self.login_pwdInput = QTextEdit(login)
        self.login_pwdInput.setObjectName(u"login_pwdInput")
        self.login_pwdInput.setMaximumSize(QSize(300, 30))

        self.gridLayout.addWidget(self.login_pwdInput, 2, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 2, 1, 1)


        self.retranslateUi(login)

        QMetaObject.connectSlotsByName(login)
    # setupUi

    def retranslateUi(self, login):
        login.setWindowTitle(QCoreApplication.translate("login", u"Form", None))
        self.login_pwd.setText(QCoreApplication.translate("login", u"\u5bc6\u7801:", None))
        self.login_id.setText(QCoreApplication.translate("login", u"\u8d26\u53f7:", None))
        self.login_message.setText(QCoreApplication.translate("login", u"message here", None))
        self.login_button.setText(QCoreApplication.translate("login", u"\u767b\u5f55", None))
        self.login_accept.setText(QCoreApplication.translate("login", u"CheckBox", None))
    # retranslateUi

