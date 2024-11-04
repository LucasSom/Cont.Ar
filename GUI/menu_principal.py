import os.path

import pandas as pd
import userpaths
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from GUI.graficos.graficos import GraficosWindow
from GUI.instrucciones.instrucciones import InstruccionesWindow
from GUI.menu_principal_ui import Ui_MainWindow
from GUI.nueva_muestra.NuevaMuestra import NuevaMuestraWindow
from GUI.sesion.Sesion import SesionWindow
from utils import cargar_archivo_muestra, error_window


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        self.nueva_muestra_w = None
        self.cargar_muestra_w = None
        self.sesion_window = None
        self.graficos_window = None
        self.instrucciones_w = None

        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.show_nueva_muestra)
        self.pushButton_2.clicked.connect(self.cargar_muestra)
        self.generarGraficosBoton.clicked.connect(self.cargar_tabla)
        self.instruccionesBoton.clicked.connect(self.instrucciones)

    def show_nueva_muestra(self):
        self.nueva_muestra_w = NuevaMuestraWindow()
        self.nueva_muestra_w.show()

    def openFileNameDialog(self, tipo='mtra'):
        fileName = None

        if tipo == 'mtra':
            fileName, _ = QFileDialog.getOpenFileName(self, "Cargar muestra", userpaths.get_my_documents(),
                                                      "Muestras (*.mtra);;All Files (*)")
        elif tipo == 'csv':
            fileName, _ = QFileDialog.getOpenFileName(self, "Cargar tabla", userpaths.get_my_documents(),
                                                      "Excel (*.xlsx);;CSV (*.csv);;All Files (*)")

        if fileName:
            return fileName
        return None

    def cargar_muestra(self, checked):
        try:
            fileName = self.openFileNameDialog()
            if fileName is not None:
                muestra = cargar_archivo_muestra(fileName)
                self.sesion_window = SesionWindow(muestra)
                self.sesion_window.show()
        except Exception as e:
            error_window(self, e)

    def cargar_tabla(self, checked):
        try:
            fileName = self.openFileNameDialog(tipo='csv')
            if fileName is not None:
                df = pd.read_csv(fileName) if os.path.splitext(fileName)[1] == '.csv' else pd.read_excel(fileName)
                df.set_index("Muestra", inplace=True)
                self.graficos_window = GraficosWindow(df, os.path.splitext(fileName)[0])
                self.graficos_window.show()
        except Exception as e:
            error_window(self, e)

    def instrucciones(self):
        self.instrucciones_w = InstruccionesWindow()
        self.instrucciones_w.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
