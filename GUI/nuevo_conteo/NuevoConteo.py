import pandas as pd
import userpaths
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from GUI.editar_mapa.EditarMapaWindow import EditarMapaWindow
from GUI.nuevo_conteo.nuevo_conteo_ui import Ui_NuevoConteoWindow
from GUI.sesion.Sesion import SesionWindow
from Muestra import Muestra
from utils.utils import guardar_muestra, error_window, warning_window, to_float


class NuevoConteoWindow(QtWidgets.QMainWindow, Ui_NuevoConteoWindow):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, nombre_tabla, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.nombre_unidad = None
        self.nombre_tabla = nombre_tabla
        self.editar_mapa_w = None
        self.sesion_window = None
        self.mapa = {}
        self.setupUi(self)
        self.cancelar_aceptar_boton.accepted.connect(self.aceptar)
        self.cancelar_aceptar_boton.rejected.connect(self.cancelar)
        self.nuevo_mapa_boton.clicked.connect(self.editar_mapa)
        self.cargar_mapa_boton.clicked.connect(self.cargar_mapa)

    def saveFileDialog(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar muestra", userpaths.get_my_documents(),
                                                  "Muestras (*.mtra);;All Files (*)")
        if file_name:
            return file_name
        return None

    def cargar_mapa(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Cargar mapa de teclas", userpaths.get_my_documents(),
                                                  "CSV (*.csv);;All Files (*)")
        if file_name:
            mapa_df = pd.read_csv(file_name)
            self.mapa = {tecla: roca[0] for tecla, roca in mapa_df.items() if type(roca[0]) is str}
            self.editar_mapa()

    def aceptar(self):
        try:
            if self.nombre_muestra.text() == '':
                warning_window(self, "El campo 'Nombre de muestra' no puede estar vacío.")
            elif self.localidad.text() == '':
                warning_window(self, "El campo 'Localidad' no puede estar vacío.")
            elif self.cantidad_lecturas.value() == 0:
                warning_window(self, "El campo 'Cantidad de lecturas' tiene que ser mayor que 0.")
            else:
                file_name = self.saveFileDialog()

                if self.nombre_unidad.text() == '':
                    nombre_unidad_texto = "Sin unidad"
                else:
                    nombre_unidad_texto = self.nombre_unidad.text()

                nueva_muestra = Muestra(self.nombre_tabla, self.localidad.text(), self.nombre_muestra.text(),
                                        nombre_unidad_texto, self.fecha.date().toPyDate(), self.operador.text(),
                                        self.cantidad_lecturas.value(), self.observaciones.toPlainText(),
                                        self.latitud.text(), self.longitud.text(),
                                        self.profundidad.value(), self.mapa, file_name)
                if file_name is not None:
                    guardar_muestra(nueva_muestra, file_name, verbose=True)

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
