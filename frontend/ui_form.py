# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        Widget.setStyleSheet(u"")
        self.frame = QFrame(Widget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 801, 601))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(60, 140, 674, 274))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)

        self.horizontalLayout_3.addWidget(self.label)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_3.addWidget(self.label_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"background-color: #e7e7e7; /* Light gray background */\n"
"color: #e7e7e7; /* Light gray background */\n"
"")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(3)
        self.line.setFrameShape(QFrame.Shape.HLine)

        self.verticalLayout.addWidget(self.line)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setPointSize(15)
        font1.setBold(True)
        self.label_3.setFont(font1)

        self.verticalLayout.addWidget(self.label_3)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_5.addWidget(self.lineEdit)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_4)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineEdit_2 = QLineEdit(self.widget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.horizontalLayout_6.addWidget(self.lineEdit_2)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        font2 = QFont()
        font2.setBold(True)
        self.pushButton_2.setFont(font2)
        self.pushButton_2.setCursor(QCursor(Qt.OpenHandCursor))
        self.pushButton_2.setMouseTracking(True)
        self.pushButton_2.setStyleSheet(u"background-color: #e7e7e7; /* Light gray background */\n"
"color: black;             /* Black text color */\n"
"border-style: solid;      /* Solid border style */\n"
"border-width: 1px;        /* Border width */\n"
"border-radius: 2px;       /* Rounded corners with a small radius */\n"
"border-color: #c6c6c6;    /* Lighter gray border */\n"
"padding: 5px;             /* Padding around the text */\n"
"font-size: 14px;          /* Text font size */")
        self.pushButton_2.setCheckable(False)

        self.horizontalLayout_7.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setFont(font2)
        self.pushButton.setCursor(QCursor(Qt.OpenHandCursor))
        self.pushButton.setMouseTracking(True)
        self.pushButton.setStyleSheet(u"background-color: #e7e7e7; /* Light gray background */\n"
"color: black;             /* Black text color */\n"
"border-style: solid;      /* Solid border style */\n"
"border-width: 1px;        /* Border width */\n"
"border-radius: 2px;       /* Rounded corners with a small radius */\n"
"border-color: #c6c6c6;    /* Lighter gray border */\n"
"padding: 5px;             /* Padding around the text */\n"
"font-size: 14px;          /* Text font size */")
        self.pushButton.setAutoDefault(False)

        self.horizontalLayout_7.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(659, 27, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)


        self.horizontalLayout.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(0, 490, 111, 111))
        self.label_5.setStyleSheet(u"background-image: url('/home/joao/QtApp/assets/icone_senha-removebg-preview.png');\n"
"background-repeat: no-repeat;\n"
"background-position: center;")

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label.setText(QCoreApplication.translate("Widget", u"LOGIN", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Sistema Supervis\u00f3rio - Monitoramento da Produ\u00e7\u00e3o de Frutas", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Usu\u00e1rio:", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"Senha:", None))
        self.pushButton_2.setText(QCoreApplication.translate("Widget", u"  Entrar  ", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Esqueci a Senha", None))
        self.label_5.setText("")
    # retranslateUi

