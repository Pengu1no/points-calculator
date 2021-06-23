# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from plot import MplWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(932, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(600, 110))
        self.groupBox.setMaximumSize(QtCore.QSize(600, 110))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.file_name = QtWidgets.QTextEdit(self.groupBox)
        self.file_name.setEnabled(True)
        self.file_name.setGeometry(QtCore.QRect(10, 10, 471, 31))
        self.file_name.setReadOnly(True)
        self.file_name.setObjectName("file_name")
        self.button_open = QtWidgets.QPushButton(self.groupBox)
        self.button_open.setGeometry(QtCore.QRect(492, 10, 101, 32))
        self.button_open.setObjectName("button_open")
        self.button_calc = QtWidgets.QPushButton(self.groupBox)
        self.button_calc.setGeometry(QtCore.QRect(10, 51, 461, 51))
        self.button_calc.setObjectName("button_calc")
        self.button_reset = QtWidgets.QPushButton(self.groupBox)
        self.button_reset.setGeometry(QtCore.QRect(480, 51, 113, 51))
        self.button_reset.setObjectName("button_reset")
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(260, 110))
        self.groupBox_2.setMaximumSize(QtCore.QSize(260, 110))
        self.groupBox_2.setObjectName("groupBox_2")
        self.file_name_excel = QtWidgets.QTextEdit(self.groupBox_2)
        self.file_name_excel.setEnabled(True)
        self.file_name_excel.setGeometry(QtCore.QRect(10, 30, 241, 31))
        self.file_name_excel.setReadOnly(True)
        self.file_name_excel.setObjectName("file_name_excel")
        self.button_open_excel = QtWidgets.QPushButton(self.groupBox_2)
        self.button_open_excel.setGeometry(QtCore.QRect(10, 70, 113, 32))
        self.button_open_excel.setObjectName("button_open_excel")
        self.button_export = QtWidgets.QPushButton(self.groupBox_2)
        self.button_export.setGeometry(QtCore.QRect(140, 70, 113, 32))
        self.button_export.setObjectName("button_export")
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plot_widget_raw = MplWidget(self.centralwidget)
        self.plot_widget_raw.setMinimumSize(QtCore.QSize(300, 300))
        self.plot_widget_raw.setObjectName("plot_widget_raw")
        self.horizontalLayout.addWidget(self.plot_widget_raw)
        self.plot_widget_res = MplWidget(self.centralwidget)
        self.plot_widget_res.setMinimumSize(QtCore.QSize(300, 300))
        self.plot_widget_res.setObjectName("plot_widget_res")
        self.horizontalLayout.addWidget(self.plot_widget_res)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.stats_text = QtWidgets.QTextEdit(self.centralwidget)
        self.stats_text.setMinimumSize(QtCore.QSize(0, 150))
        self.stats_text.setMaximumSize(QtCore.QSize(16777215, 150))
        self.stats_text.setReadOnly(True)
        self.stats_text.setObjectName("stats_text")
        self.verticalLayout_2.addWidget(self.stats_text)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_settings = QtWidgets.QAction(MainWindow)
        self.action_settings.setObjectName("action_settings")
        self.toolBar.addAction(self.action_settings)
        self.action_legend = QtWidgets.QAction(MainWindow)
        self.action_legend.setObjectName("action_legend")
        self.toolBar.addAction(self.action_legend)
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.toolBar.addAction(self.action_about)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Расчёт точек"))
        self.button_open.setText(_translate("MainWindow", "Открыть"))
        self.button_calc.setText(_translate("MainWindow", "Рассчитать"))
        self.button_reset.setText(_translate("MainWindow", "Сбросить"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Выгрузка в Excel"))
        self.button_open_excel.setText(_translate("MainWindow", "Выбрать"))
        self.button_export.setText(_translate("MainWindow", "Выгрузить"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_settings.setText(_translate("MainWindow", "Настройки"))
        self.action_legend.setText(_translate("MainWindow", "Легенда"))
        self.action_about.setText(_translate("MainWindow", "Справка"))
