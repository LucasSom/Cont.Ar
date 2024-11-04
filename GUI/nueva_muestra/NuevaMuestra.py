import pandas as pd
import userpaths
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from GUI.editar_mapa.EditarMapaWindow import EditarMapaWindow
from GUI.nueva_muestra.nueva_muestra_ui import Ui_NuevaMuestraWindow
from GUI.sesion.Sesion import SesionWindow
from Muestra import Muestra
from utils import guardar_muestra, error_window, warning_window


class NuevaMuestraWindow(QtWidgets.QMainWindow, Ui_NuevaMuestraWindow):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.editar_mapa_w = None
        self.sesion_window = None
        self.mapa = {}
        self.setupUi(self)
        self.cancelar_aceptar_boton.accepted.connect(self.aceptar)
        self.cancelar_aceptar_boton.rejected.connect(self.cancelar)
        self.nuevo_mapa_boton.clicked.connect(self.editar_mapa)
        self.cargar_mapa_boton.clicked.connect(self.cargar_mapa)

    def saveFileDialog(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Guardar muestra", userpaths.get_my_documents(),
                                                  "Muestras (*.mtra);;All Files (*)")
        if fileName:
            return fileName
        return None

    def cargar_mapa(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Cargar mapa de teclas", userpaths.get_my_documents(),
                                                  "CSV (*.csv);;All Files (*)")
        if fileName:
            mapa_df = pd.read_csv(fileName)
            self.mapa = {tecla: roca[0] for tecla, roca in mapa_df.items() if type(roca[0]) is str}
            self.editar_mapa()

    def aceptar(self):
        if self.nombre.text() == '':
            warning_window(self, "El campo 'Nombre' no puede estar vacío.")
        elif self.localidad.text() == '':
            warning_window(self, "El campo 'Localidad' no puede estar vacío.")
        elif self.cantidad_lecturas.value() == 0:
            warning_window(self, "El campo 'Cantidad de lecturas' tiene que ser mayor que 0.")
        else:
            fileName = self.saveFileDialog()
            nueva_muestra = Muestra(self.nombre.text(),
                                    self.fecha.date().toPyDate(),
                                    self.localidad.text(),
                                    self.operador.text(),
                                    self.cantidad_lecturas.value(),
                                    self.observaciones.toPlainText(),
                                    self.mapa,
                                    fileName)
            if fileName is not None:
                guardar_muestra(nueva_muestra, fileName, verbose=True)

                try:
                    self.sesion_window = SesionWindow(nueva_muestra)
                    self.sesion_window.show()
                except Exception as e:
                    error_window(self, e)
                self.close()

    def cancelar(self):
        self.close()

    def editar_mapa(self):
        self.editar_mapa_w = EditarMapaWindow(self)
        self.editar_mapa_w.show()
