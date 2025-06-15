import os
import pickle

import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

project_path = os.path.dirname(os.path.abspath(__file__))


def file_extension(p):
    return os.path.splitext(p)[1]


def guardar_muestra(obj, file_name: str, verbose=False):
    if file_extension(file_name) != '.mtra':
        file_name += '.mtra'

    directory = os.path.dirname(file_name)
    if not os.path.isdir(directory) and directory != '':
        os.makedirs(directory)
        if verbose: print("Created directory:", directory)

    with open(file_name, 'wb') as f:
        pickle.dump(obj, f)
        if verbose: print("Saved as:", file_name)


def cargar_archivo_muestra(file_name: str, verbose=False):
    if file_extension(file_name) != '.mtra':
        file_name += '.mtra'

    with open(file_name, 'rb') as f:
        p = pickle.load(f)
        if verbose: print("Loaded file:", f)
        return p


def filtrar_tipo_roca(df: pd.DataFrame, tipo: str) -> pd.DataFrame:
    columnas = [c for c in df.columns if c[1:len(tipo) + 1] == tipo]
    df_sum = df[columnas].sum(axis=1)
    df_sum.index = df.index
    return df_sum


def error_window(parent, e: Exception):
    exception_pop_up = QMessageBox(parent)
    exception_pop_up.setText(f"Se ha producido el siguiente error:\n{e}")
    exception_pop_up.setIcon(QMessageBox.Critical)
    exception_pop_up.exec()


def warning_window(parent, texto):
    warning_pop_up = QMessageBox(parent)
    warning_pop_up.setText(texto)
    warning_pop_up.setIcon(QMessageBox.Warning)
    warning_pop_up.exec()


def info_window(parent, texto):
    information_pop_up = QMessageBox(parent)
    information_pop_up.setText(texto)
    information_pop_up.setIcon(QMessageBox.Information)
    information_pop_up.exec()


def values_unicity_check(parent, mapa):
    rocas = [r for r in mapa.values() if r != '']
    if len(rocas) != len(set(rocas)):
        warning_window(parent, "Hay valores duplicados.")
        return False
    return True


def es_tabla_legacy(file_name: str) -> bool:
    df = pd.read_excel(file_name)
    return 'Localidad' not in df.columns


def to_float(value):
    if value:
        value = str(value).replace(',', '.')
        return float(value)
    return np.nan

def columnas_rocas(df):
    return [c for c in df.columns if c not in ["Latitud", "Longitud", "Profundidad"]]
