import sys
from functools import partial
from pathlib import Path

from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QColorDialog
from PyQt5.QtCore import QDir, QObject, pyqtSignal, pyqtProperty, QUrl

import matplotlib

import interface

from interface_settings import Ui_Dialog as SettingsDialog
from interface_about import Ui_Dialog as AboutDialog

from calc import process_file, excel_export, predict_types, raw_types, prediction
from settings import Settings, ICON_DIR, BASE_DIR

matplotlib.use('Qt5Agg')


class SettingsDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = SettingsDialog()
        self.ui.setupUi(self)

        self.proj_settings = Settings()

        self.ui.background_color.setText(self.proj_settings.background_color)
        self.ui.background_pick.clicked.connect(partial(self.pick_color, 'background_color'))

        for k, v in self.proj_settings.types_match.items():
            color = self.ui.__getattribute__(f'type{k}_color')
            marker = self.ui.__getattribute__(f'type{k}_marker')
            name = self.ui.__getattribute__(f'type{k}_name')

            pick = self.ui.__getattribute__(f'type{k}_pick')

            marker_idx = marker.findText(self.proj_settings.markers[self.proj_settings.types_match[k][0]].stem)
            marker.setCurrentIndex(marker_idx)
            color.setText(self.proj_settings.types_match[k][1])
            name.setText(self.proj_settings.types_match[k][2])

            pick.clicked.connect(partial(self.pick_color, f'type{k}_color'))

        self.ui.buttonBox.accepted.connect(self.apply)

    def apply(self):
        plot_settings = {}

        for k, v in self.proj_settings.types_match.items():
            color = self.ui.__getattribute__(f'type{k}_color')
            marker = self.ui.__getattribute__(f'type{k}_marker')
            name = self.ui.__getattribute__(f'type{k}_name')

            marker_text = marker.currentText()
            marker_value = self.proj_settings.markers_rev[ICON_DIR / f'{marker_text}.png']

            color_text = color.toPlainText()
            color_value = color_text

            name_text = name.toPlainText()

            plot_settings[k] = [marker_value, color_value, name_text]

        self.proj_settings.save_type_match(plot_settings)
        bg = self.ui.background_color.toPlainText()
        self.proj_settings.save_background_color(bg)
        self.parent().plot_widget_raw.set_background(bg)
        self.parent().plot_widget_res.set_background(bg)
        self.parent().redraw_raw()
        self.parent().redraw_calc()

    def pick_color(self, t):
        color_box = self.ui.__getattribute__(t)
        color_value = color_box.toPlainText()

        color = QColorDialog.getColor(QColor(color_value))
        color_box.setText(color.name())


class AboutDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = AboutDialog()
        self.ui.setupUi(self)

        url = QUrl.fromLocalFile(str(BASE_DIR / 'README.html'))
        self.ui.widget_about.load(url)


class Application(QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле interface.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.proj_settings = Settings()

        self._export_data = None

        self._file_data = {
            'data': None,
            'test': None,
            'x_test': None,
            '_Y_test': None,
            'Y_pred': None,
        }

        self.legend_visible = True
        self.fullscreen = {
            'raw': False,
            'res': False,
            'about': False,
        }

        self.cw = self.centralwidget

        self.view = QWebEngineView()
        url = QUrl.fromLocalFile(str(BASE_DIR / 'README.html'))
        self.view.load(url)

        self.plot_widget_raw.set_background(self.proj_settings.background_color)
        self.plot_widget_res.set_background(self.proj_settings.background_color)

        self.button_open.clicked.connect(self.browse_files)
        self.button_open_excel.clicked.connect(self.browse_export)
        self.button_export.clicked.connect(self.export)
        self.button_calc.clicked.connect(self.calc_plot)
        self.button_reset.clicked.connect(self.reset_calc)
        self.action_settings.triggered.connect(self.open_settings_dialog)
        self.action_legend.triggered.connect(self.toggle_legend)
        self.action_about.triggered.connect(self.open_about_dialog)

        self.plot_widget_raw.canvas.toggle.connect(self.fullscreen_plot_raw)
        self.plot_widget_res.canvas.toggle.connect(self.fullscreen_plot_res)

    def fullscreen_plot_raw(self):
        if not self.fullscreen['raw']:
            self.cw.setParent(None)
            self.setCentralWidget(self.plot_widget_raw)
            self.fullscreen['raw'] = True
        else:
            self.plot_widget_raw.setParent(None)
            self.horizontalLayout.insertWidget(0, self.plot_widget_raw)
            self.setCentralWidget(self.cw)
            self.fullscreen['raw'] = False

    def fullscreen_plot_res(self):
        if not self.fullscreen['res']:
            self.cw.setParent(None)
            self.setCentralWidget(self.plot_widget_res)
            self.fullscreen['res'] = True
        else:
            self.plot_widget_res.setParent(None)
            self.horizontalLayout.insertWidget(1, self.plot_widget_res)
            self.setCentralWidget(self.cw)
            self.fullscreen['res'] = False

    def toggle_buttons(self, disabled):
        self.button_open.setDisabled(disabled)
        self.button_calc.setDisabled(disabled)
        self.button_reset.setDisabled(disabled)
        self.button_open_excel.setDisabled(disabled)
        self.button_export.setDisabled(disabled)

    def toggle_legend(self):
        self.legend_visible = not self.legend_visible
        self.redraw_raw()
        self.redraw_calc()

    def open_settings_dialog(self):
        dlg = SettingsDlg(self)
        dlg.exec()

    def open_about_dialog(self):
        dlg = AboutDlg(self)
        dlg.exec()

    def browse_files(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Выберите файл с координатами', QDir.rootPath(), '*.xyz')

        if filename:
            self._file_data = {
                'data': None,
                'test': None,
                'x_test': None,
                '_Y_test': None,
                'Y_pred': None,
            }

            self.file_name.setText(filename)

            self._file_data = process_file(Path(filename))
            self.reset_calc()
            self.redraw_raw()

    def browse_export(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Выберите файл для выгрузки', QDir.rootPath(), '*.xlsx')

        if filename:
            self.file_name_excel.setText(filename)

    def export(self):
        _translate = QtCore.QCoreApplication.translate
        self.button_export.setText(_translate("MainWindow", "Выгружается"))
        path = Path(self.file_name_excel.toPlainText())
        excel_export(path, *self._export_data)
        self.button_export.setText(_translate("MainWindow", "Выгрузить"))

    def redraw_raw(self):
        self.reset_raw()
        if self._file_data['data'] is not None:
            plot_data, legend, z_lim, export = raw_types(self._file_data)
            legend = legend if self.legend_visible else None

            background = self.proj_settings.background_color
            self.plot_widget_raw.draw_plot(plot_data, legend, background, z_lim)

    def redraw_calc(self):
        if self._file_data.get('Y_pred') is not None:
            self.reset_calc()
            plot_data, legend, z_lim, export, report = predict_types(self._file_data)
            legend = legend if self.legend_visible else None
            self._export_data = export
            self.stats_text.setText(report)

            background = self.proj_settings.background_color
            self.plot_widget_res.draw_plot(plot_data, legend, background, z_lim)

    def reset_raw(self):
        self.stats_text.clear()
        self.plot_widget_raw.canvas.axes.clear()
        self.plot_widget_raw.canvas.draw()

    def reset_calc(self):
        self._export_data = None
        self.stats_text.clear()
        self.plot_widget_res.canvas.axes.clear()
        self.plot_widget_res.canvas.draw()

    def calc_plot(self):
        self.reset_calc()
        self._file_data['Y_pred'] = prediction(self._file_data['x_test'])
        self.redraw_calc()


def main():
    app = QApplication(sys.argv)
    window = Application()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
