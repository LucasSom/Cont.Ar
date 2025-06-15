import os.path

import pandas as pd
import userpaths
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from GUI.graficos.graficos import GraficosWindow
from GUI.instrucciones.instrucciones import InstruccionesWindow
from GUI.menu_principal_ui import Ui_MainWindow
from GUI.nuevo_conteo.NuevoConteo import NuevoConteoWindow
from GUI.sesion.Sesion import SesionWindow
from utils import cargar_archivo_muestra, error_window, file_extension


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        self.nuevo_conteo_w = None
        self.cargar_conteo_w = None
        self.sesion_window = None
        self.graficos_window = None
        self.instrucciones_w = None

        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.nuevoConteoButton.clicked.connect(self.show_nuevo_conteo)
        self.cargarConteoButton.clicked.connect(self.cargar_conteo)
        self.generarGraficosBoton.clicked.connect(self.cargar_tabla)
        self.instruccionesBoton.clicked.connect(self.instrucciones)

    def show_nuevo_conteo(self):
        nombre_tabla = self.saveFileDialog()

        if nombre_tabla is not None:
            self.nuevo_conteo_w = NuevoConteoWindow(nombre_tabla)
            self.nuevo_conteo_w.show()

    def saveFileDialog(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Cargar o crear tabla", userpaths.get_my_documents(),
                                                  "Excel Open XML Spreadsheet (*.xlsx);;Excel Spreadsheet (*.xls);;CSV (*.csv);;All Files (*)")

        if not file_extension(file_name):
            file_name = f"{file_name}.xlsx"

        if file_name:
            return file_name
        return None

    def openFileNameDialog(self, tipo='mtra'):
        file_name = None

        if tipo == 'mtra':
            file_name, _ = QFileDialog.getOpenFileName(self, "Cargar conteo", userpaths.get_my_documents(),
                                                      "Muestras (*.mtra);;All Files (*)")
        elif tipo in ('csv', 'xlsx'):
            file_name, _ = QFileDialog.getOpenFileName(self, "Cargar tabla", userpaths.get_my_documents(),
                                                      "Excel Open XML Spreadsheet (*.xlsx);;Excel Spreadsheet (*.xls);;CSV (*.csv);;All Files (*)")

        if file_name:
            return file_name
        return None

    def cargar_conteo(self, checked):
        try:
            file_name = self.openFileNameDialog()
            if file_name is not None:
                muestra = cargar_archivo_muestra(file_name)
                self.sesion_window = SesionWindow(muestra)
                self.sesion_window.show()
        except Exception as e:
            error_window(self, e)

    def cargar_tabla(self, checked):
        try:
            file_name = self.openFileNameDialog(tipo='csv')
            if file_name is not None:
                df = pd.read_csv(file_name) if file_extension(file_name) == '.csv' else pd.read_excel(file_name)

                indices_posibles = ["Localidad", "Muestra", "Unidad"]
                indices = []
                for i in indices_posibles:
                    if i in df.columns:
                        indices.append(i)
                if 'Localidad' in df.columns:
                    # Llenamos los valores nulos de Localidad hacia adelante
                    df['Localidad'].ffill(inplace=True)
                    # Dejamos el último valor de Localidad como None
                    df.loc[df.shape[0] - 1, 'Localidad'] = None
                df.set_index(indices, inplace=True)

                self.graficos_window = GraficosWindow(df, os.path.splitext(file_name)[0])
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
