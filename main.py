import requests
from PyQt5 import QtWidgets

from GUI.menu_principal import MainWindow
from utils import info_window


def check_for_update(current_version, w):
    try:
        response = requests.get("https://api.github.com/repos/LucasSom/Cont.Ar/releases/latest")
        latest_version = response.json()["tag_name"]

        if current_version < latest_version:
            notify_user(latest_version, w)
    except Exception as e:
        if type(e) is requests.exceptions.ConnectionError:
            info_window(w, "No se pudieron comprobar actualizaciones por problemas de conexión.")
        else:
            print(e)
            info_window(w, f"No se pudieron comprobar actualizaciones por el error:\n{e}.")


def notify_user(latest_version, w):
    info_window(w, f"Hay una nueva versión disponible: {latest_version}.\n"
                   f"Actualizar descargando de https://github.com/LucasSom/Cont.Ar")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    check_for_update("v1.1", window)
    window.show()
    app.exec_()
