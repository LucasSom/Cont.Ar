import os

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets


class Ui_Instrucciones(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)

        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.centralwidget = QtWidgets.QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webEngineView.load(QtCore.QUrl().fromLocalFile(os.path.join(os.path.split(os.path.abspath(__file__))[0],
                                                                         'instrucciones.html')))
        self.verticalLayout.addWidget(self.webEngineView)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.verticalLayout.addWidget(self.buttonBox)
        self.retranslateUi(Dialog)

        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Instrucciones"))


class InstruccionesWindow(QtWidgets.QDialog, Ui_Instrucciones, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Instrucciones()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
