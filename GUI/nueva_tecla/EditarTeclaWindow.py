from GUI.nueva_tecla.nueva_tecla_ui import Ui_Dialog_Editar_Tecla
from PyQt5 import QtWidgets

from utils import values_unicity_check


class EditarTeclaWindow(QtWidgets.QDialog, Ui_Dialog_Editar_Tecla):
    def __init__(self, parent=None):
        super(EditarTeclaWindow, self).__init__()
        self.parent = parent
        self.setupUi(self)
        self.aceptar_cancelar.accepted.connect(self.editar_tecla)

    def editar_tecla(self):
        tecla = self.tecla_input.text().upper()
        nombre_roca = self.componente_input.text()
        self.parent.muestra.mapa[tecla] = nombre_roca

        if values_unicity_check(self.parent, self.parent.muestra.mapa):
            self.parent.imprimir_lista_teclas()
            self.parent.nueva_fila_contador(nombre_roca)
            self.close()
