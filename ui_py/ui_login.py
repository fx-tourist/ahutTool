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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_login(object):
    def setupUi(self, login):
        if not login.objectName():
            login.setObjectName(u"login")
        login.resize(533, 552)
        self.gridLayout = QGridLayout(login)
        self.gridLayout.setObjectName(u"gridLayout")
        self.login_id = QLabel(login)
        self.login_id.setObjectName(u"login_id")
        self.login_id.setMaximumSize(QSize(150, 30))
        self.login_id.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.login_id, 1, 1, 1, 1)

        self.used_accept = QCheckBox(login)
        self.used_accept.setObjectName(u"used_accept")

        self.gridLayout.addWidget(self.used_accept, 3, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 4, 1, 1)

        self.login_pwdInput = QLineEdit(login)
        self.login_pwdInput.setObjectName(u"login_pwdInput")
        self.login_pwdInput.setMinimumSize(QSize(200, 0))
        self.login_pwdInput.setMaxLength(15)
        self.login_pwdInput.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_pwdInput.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.login_pwdInput, 2, 3, 1, 1)

        self.messageShow = QLabel(login)
        self.messageShow.setObjectName(u"messageShow")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messageShow.sizePolicy().hasHeightForWidth())
        self.messageShow.setSizePolicy(sizePolicy)
        self.messageShow.setMaximumSize(QSize(16777215, 16777215))
        self.messageShow.setLineWidth(999)
        self.messageShow.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.messageShow.setWordWrap(True)

        self.gridLayout.addWidget(self.messageShow, 7, 3, 1, 1)

        self.login_button = QPushButton(login)
        self.login_button.setObjectName(u"login_button")

        self.gridLayout.addWidget(self.login_button, 6, 3, 1, 1)

        self.login_idInput = QLineEdit(login)
        self.login_idInput.setObjectName(u"login_idInput")
        self.login_idInput.setMinimumSize(QSize(200, 0))
        self.login_idInput.setMaxLength(15)
        self.login_idInput.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.login_idInput, 1, 3, 1, 1)

        self.login_pwd = QLabel(login)
        self.login_pwd.setObjectName(u"login_pwd")
        self.login_pwd.setMaximumSize(QSize(150, 30))
        self.login_pwd.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout.addWidget(self.login_pwd, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(90, 90, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 8, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.loginBg = QLabel(login)
        self.loginBg.setObjectName(u"loginBg")
        sizePolicy.setHeightForWidth(self.loginBg.sizePolicy().hasHeightForWidth())
        self.loginBg.setSizePolicy(sizePolicy)
        self.loginBg.setMinimumSize(QSize(0, 120))

        self.gridLayout.addWidget(self.loginBg, 0, 3, 1, 1)


        self.retranslateUi(login)

        QMetaObject.connectSlotsByName(login)
    # setupUi

    def retranslateUi(self, login):
        login.setWindowTitle(QCoreApplication.translate("login", u"Form", None))
        self.login_id.setText(QCoreApplication.translate("login", u"\u8d26\u53f7:", None))
        self.used_accept.setText(QCoreApplication.translate("login", u"CheckBox", None))
        self.login_pwdInput.setText(QCoreApplication.translate("login", u"20060612", None))
        self.messageShow.setText("")
        self.login_button.setText(QCoreApplication.translate("login", u"\u767b\u5f55", None))
        self.login_idInput.setText(QCoreApplication.translate("login", u"249074144", None))
        self.login_pwd.setText(QCoreApplication.translate("login", u"\u5bc6\u7801:", None))
        self.loginBg.setText("")
    # retranslateUi

