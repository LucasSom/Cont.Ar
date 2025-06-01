from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QTableWidget, QListWidget

from GUI.nueva_tecla.EditarTeclaWindow import EditarTeclaWindow
from GUI.sesion.sesion_ui import Ui_Dialog_Sesion
from utils import guardar_muestra, error_window, info_window


class SesionWindow(QtWidgets.QDialog, Ui_Dialog_Sesion, QtWidgets.QWidget):
    def __init__(self, muestra):
        try:
            super(SesionWindow, self).__init__()
            self.muestra = muestra
            self.nueva_tecla_window = None
            self.setupUi(self)

            self.deshacerButton.clicked.connect(self.borrar_roca)
            self.agregarTeclaButton.clicked.connect(self.agregar_tecla)
            self.guardarButton.clicked.connect(self.guardar)

            self.widget_tabla.focusOutEvent = self.on_table_widget_focus_out
            self.widget_mapa.focusOutEvent = self.on_list_widget_focus_out
            self.widget_rocas.focusOutEvent = self.on_list_widget_focus_out

        except Exception as e:
            error_window(self, e)

    def keyPressEvent(self, event):
        try:
            tecla = event.text()
            if event.key() == Qt.Key_Escape:
                self.cancelar()
            elif event.key() in [Qt.Key_Backspace, Qt.Key_Delete]:
                self.borrar_roca()
            elif tecla.isalnum():
                roca = self.muestra.mapa[tecla.upper()]
                if roca != "":
                    self.agregar_roca(roca)
                else:
                    info_window(self, f"La tecla {tecla.upper()} no tiene nigún componente asociado.")
        except Exception as e:
            error_window(self, e)

    def focusInEvent(self, event):
        self.setFocus(Qt.ActiveWindowFocusReason)
        super().focusInEvent(event)

    def on_table_widget_focus_out(self, event):
        self.setFocus(Qt.ActiveWindowFocusReason)
        super(QTableWidget, self.widget_tabla).focusOutEvent(event)

    def on_list_widget_focus_out(self, event):
        self.setFocus(Qt.ActiveWindowFocusReason)
        super(QListWidget, self.widget_tabla).focusOutEvent(event)

    def agregar_roca(self, roca):
        try:
            self.listwidgetRocas.insertItem(0, roca)
            self.incrementar_contador(roca)

            if self.listwidgetRocas.count() >= self.muestra.cantidad_lecturas:
                self.guardar()

                finalizarPopUp = QMessageBox(self)
                finalizarPopUp.setText(f"Sesión finalizada.\n"
                                       f"Se llegó a los {self.muestra.cantidad_lecturas} conteos.\n"
                                       f"Se procederá a calcular los resultados correspondientes.")
                finalizarPopUp.setIcon(QMessageBox.Information)
                finalizarPopUp.exec()

                mapa_file_name = self.muestra.exportar_datos()

                info_window(self, f"Se guardó la tabla de resultados en:\n{mapa_file_name}")

                self.close()
            else:
                self.guardar()
        except Exception as e:
            error_window(self, e)

    def incrementar_contador(self, componente):
        n_filas = self.tableView.rowCount()
        for i in range(n_filas):
            if componente == self.tableView.item(i, 0).text():
                cantidad = int(self.tableView.item(i, 1).text()) + 1
                self.tableView.setItem(i, 1, QtWidgets.QTableWidgetItem(str(cantidad)))
                break
        self.tableView.item(n_filas - 1, 1).setText(str(int(self.tableView.item(n_filas - 1, 1).text()) + 1))

    def agregar_tecla(self):
        self.nueva_tecla_window = EditarTeclaWindow(self)
        self.nueva_tecla_window.show()

    def nueva_fila_contador(self, nombre_roca):
        ultima_fila = self.tableView.rowCount()
        self.tableView.insertRow(ultima_fila - 1)
        self.tableView.setItem(ultima_fila - 1, 0, QtWidgets.QTableWidgetItem(nombre_roca))
        self.tableView.setItem(ultima_fila - 1, 1, QtWidgets.QTableWidgetItem('0'))
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()

    def borrar_roca(self):
        n_filas = self.tableView.rowCount()
        item = self.listwidgetRocas.takeItem(0)
        for i in range(n_filas):
            if item.text() == self.tableView.item(i, 0).text():
                cantidad = int(self.tableView.item(i, 1).text()) - 1
                self.tableView.setItem(i, 1, QtWidgets.QTableWidgetItem(str(cantidad)))
                break
        self.tableView.item(n_filas - 1, 1).setText(str(int(self.tableView.item(n_filas - 1, 1).text()) - 1))

    def guardar(self):
        self.muestra.componentes = [self.listwidgetRocas.item(i).text() for i in range(self.listwidgetRocas.count())]
        guardar_muestra(self.muestra, self.muestra.file_name)
