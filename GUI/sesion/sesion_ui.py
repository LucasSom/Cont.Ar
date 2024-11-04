# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/sesion/sesion.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSizePolicy


class Ui_Dialog_Sesion(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(930, 815)

        self.guardarButton = QtWidgets.QCommandLinkButton(self.Dialog)
        self.guardarButton.setGeometry(QtCore.QRect(900, 760, 171, 50))
        self.guardarButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        # self.aceptar_cancelar.setOrientation(QtCore.Qt.Horizontal)
        # self.aceptar_cancelar.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Save)
        self.guardarButton.setObjectName("aceptar_cancelar")

        self.deshacerButton = QtWidgets.QCommandLinkButton(self.Dialog)
        self.deshacerButton.setGeometry(QtCore.QRect(10, 760, 530, 50))
        self.deshacerButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.deshacerButton.setObjectName("deshacerButton")

        self.agregarTeclaButton = QtWidgets.QCommandLinkButton(self.Dialog)
        self.agregarTeclaButton.setGeometry(QtCore.QRect(550, 760, 350, 50))
        self.agregarTeclaButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.agregarTeclaButton.setObjectName("agregarTeclaButton")

        # Layout principal
        main_layout = QtWidgets.QVBoxLayout(self.Dialog)
        content_layout = QtWidgets.QHBoxLayout()  # Layout horizontal para dividir la parte izquierda y derecha
        middle_layout = QtWidgets.QVBoxLayout()  # Para las áreas de scroll al medio
        left_layout = QtWidgets.QVBoxLayout()  # Para las áreas de scroll a la izquierda
        right_layout = QtWidgets.QVBoxLayout()  # Para la tabla a la derecha

        # Scroll area de las rocas
        self.scrollRocas = QtWidgets.QScrollArea(self.Dialog)
        self.scrollRocas.setGeometry(QtCore.QRect(0, 530, 551, 221))
        self.scrollRocas.setWidgetResizable(True)
        self.scrollRocas.setObjectName("scrollRocas")

        self.scrollRocasWidgetContents = QtWidgets.QWidget()
        self.scrollRocasWidgetContents.setGeometry(QtCore.QRect(0, 0, 549, 219))
        self.scrollRocasWidgetContents.setObjectName("scrollRocasWidgetContents")
        self.scrollRocas.setWidget(self.scrollRocasWidgetContents)

        self.vbox_rocas = QtWidgets.QVBoxLayout(self.scrollRocasWidgetContents)  # The Vertical Box that contains the Horizontal Boxes of labels and buttons
        self.widget_rocas = QtWidgets.QWidget()  # Widget that contains the collection of Vertical Box

        self.listwidgetRocas = QtWidgets.QListWidget()
        for roca in self.Dialog.muestra.componentes:
            self.listwidgetRocas.addItem(roca)
        self.vbox_rocas.addWidget(self.listwidgetRocas)
        self.widget_rocas.setLayout(self.vbox_rocas)
        self.scrollRocas.setWidget(self.widget_rocas)
        left_layout.addWidget(self.scrollRocas)
        # left_layout.addStretch(1)

        # self.editarMapaBoton = QtWidgets.QPushButton(self.Dialog)
        # self.editarMapaBoton.setGeometry(QtCore.QRect(560, 760, 511, 31))
        # self.editarMapaBoton.setObjectName("editarMapaBoton")

        self.scrollMapa = QtWidgets.QScrollArea(self.Dialog)
        self.scrollMapa.setGeometry(QtCore.QRect(0, 0, 551, 521))
        self.scrollMapa.setWidgetResizable(True)
        self.scrollMapa.setObjectName("scrollMapa")

        self.scrollMapaWidgetContents = QtWidgets.QWidget()
        self.scrollMapaWidgetContents.setGeometry(QtCore.QRect(0, 0, 549, 519))
        self.scrollMapaWidgetContents.setObjectName("scrollMapaWidgetContents")

        # Scroll area del mapa de teclas
        self.vbox_mapa = QtWidgets.QVBoxLayout(self.scrollMapaWidgetContents)  # The Vertical Box that contains the Horizontal Boxes of labels and buttons
        self.widget_mapa = QtWidgets.QWidget()  # Widget that contains the collection of Vertical Box

        self.listwidgetMapa = QtWidgets.QListWidget()
        self.imprimir_lista_teclas()
        self.vbox_mapa.addWidget(self.listwidgetMapa)
        self.widget_mapa.setLayout(self.vbox_mapa)
        self.scrollMapa.setWidget(self.widget_mapa)
        # self.scrollMapa.setWidget(self.scrollMapaWidgetContents)
        middle_layout.addWidget(self.scrollMapa)
        # middle_layout.addStretch(1)

        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

        # scroll area de la tabla de conteo de rocas
        self.scrollTableArea = QtWidgets.QScrollArea(self.Dialog)
        self.scrollTableArea.setGeometry(QtCore.QRect(560, 0, 511, 751))
        self.scrollTableArea.setWidgetResizable(True)
        self.scrollTableArea.setObjectName("scrollTableArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 509, 749))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollTableArea.setWidget(self.scrollAreaWidgetContents)

        self.vbox_tabla = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)  # The Vertical Box that contains the Horizontal Boxes of labels and buttons
        self.widget_tabla = QtWidgets.QWidget()  # Widget that contains the collection of Vertical Box

        self.tableView = QtWidgets.QTableWidget()
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableView.setColumnCount(2)
        self.tableView.setRowCount(len([componente for componente in self.Dialog.muestra.mapa.values()
                                        if componente != '']) + 1)
        self.tableView.setGeometry(QtCore.QRect(560, 0, 517, 747))
        self.tableView.setObjectName("tablaConteo")
        self.tableView.verticalHeader().setVisible(False)
        self.imprimir_conteo_inicial()
        self.vbox_tabla.addWidget(self.tableView)
        self.widget_tabla.setLayout(self.vbox_tabla)
        self.scrollTableArea.setWidget(self.widget_tabla)
        right_layout.addWidget(self.scrollTableArea)
        # right_layout.addStretch(1)

        # Añadir layouts de izquierda y derecha al layout de contenido
        content_layout.addLayout(left_layout)
        content_layout.addLayout(middle_layout)
        content_layout.addLayout(right_layout)
        content_layout.addStretch(1)
        main_layout.addLayout(content_layout)

        # Layout para los botones
        buttons_layout = QtWidgets.QGridLayout(self.Dialog)
        ac_layout = QtWidgets.QHBoxLayout(self.Dialog)
        des_layout = QtWidgets.QHBoxLayout(self.Dialog)
        ag_layout = QtWidgets.QHBoxLayout(self.Dialog)
        # buttons_layout.addWidget(self.imagen)
        ac_layout.addWidget(self.guardarButton)
        des_layout.addWidget(self.deshacerButton)
        ag_layout.addWidget(self.agregarTeclaButton)
        buttons_layout.addLayout(des_layout, 0, 0)
        buttons_layout.addLayout(ag_layout, 0, 1)
        buttons_layout.addLayout(ac_layout, 0, 2)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Añadir el layout de botones al layout principal
        main_layout.addLayout(buttons_layout)
        main_layout.setAlignment(Qt.AlignLeft)

        self.retranslateUi()

    def imprimir_lista_teclas(self):
        i = 0
        self.listwidgetMapa.clear()
        for tecla, roca in sorted(list(self.Dialog.muestra.mapa.items())):
            if roca != "":
                self.listwidgetMapa.addItem(f"{tecla}: {roca}")
                item = self.listwidgetMapa.item(i)
                i += 1

    def imprimir_conteo_inicial(self):
        componentes = self.Dialog.muestra.getComponentesCount()
        total = 0
        for i, (componente, cantidad) in enumerate(componentes.items()):
            self.tableView.setItem(i, 0, QtWidgets.QTableWidgetItem(componente))
            self.tableView.setItem(i, 1, QtWidgets.QTableWidgetItem(str(cantidad)))
            total += cantidad
        i = len(componentes)
        self.tableView.setItem(i, 0, QtWidgets.QTableWidgetItem("Total"))
        self.tableView.setItem(i, 1, QtWidgets.QTableWidgetItem(str(total)))
        self.tableView.resizeColumnsToContents()
        self.tableView.resizeRowsToContents()
        self.tableView.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.Dialog.setWindowTitle(_translate("Dialog", "Sesión"))
        self.deshacerButton.setText(_translate("Dialog", "Deshacer"))
        self.agregarTeclaButton.setText(_translate("Dialog", "Agregar tecla"))
        self.guardarButton.setText(_translate("Dialog", "Guardar"))
        # self.label.setText(_translate("Dialog", "Input"))
        # self.editarMapaBoton.setText(_translate("Dialog", "Editar mapa de teclas"))
