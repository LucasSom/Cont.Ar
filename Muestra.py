import os
from collections import Counter
from typing import Dict

import pandas as pd

from diagrama import nombre_clasificacion
from utils import es_tabla_legacy, columnas_rocas


class Muestra:
    def __init__(self, nombre_tabla, localidad, nombre_muestra, nombre_unidad, fecha, operador, cantidad_lecturas,
                 observaciones, latitud, longitud, profundidad, mapa, file_name):
        self.nombre_tabla = nombre_tabla
        self.nombre_muestra = str(nombre_muestra)
        self.nombre_unidad = str(nombre_unidad)
        self.fecha = fecha
        self.localidad = localidad
        self.operador = operador
        self.cantidad_lecturas = cantidad_lecturas
        self.observaciones = observaciones
        self.latitud = latitud
        self.longitud = longitud
        self.profundidad = profundidad
        self.mapa = mapa
        self.file_name = file_name
        self.componentes = []

    def exportar_datos(self):
        path_dir = os.path.dirname(self.file_name)
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        df_new = pd.DataFrame(self.componentes, columns=["Muestra"])
        counts_df = pd.DataFrame(df_new["Muestra"].value_counts(normalize=True) * 100)
        df_new = counts_df.rename(columns={"proportion": self.nombre_muestra}).T
        # df_new.rename(index={'Muestra': self.nombre_muestra}, inplace=True)
        df_new["Localidad"] = [self.localidad]
        df_new["Muestra"] = [self.nombre_muestra]
        df_new["Unidad"] = [self.nombre_unidad]
        df_new["Latitud"] = [self.latitud]
        df_new["Longitud"] = [self.longitud]
        df_new["Profundidad"] = [self.profundidad]
        df_new.set_index(["Localidad", "Muestra", "Unidad"], inplace=True)
        df_new = df_new[["Latitud", "Longitud", "Profundidad"] + columnas_rocas(df_new)]

        # Cargar viejo Excel y concatenarlo
        if os.path.isfile(self.nombre_tabla):
            # Determino si la tabla es legacy o no
            if es_tabla_legacy(self.nombre_tabla):
                df_old = pd.read_excel(self.nombre_tabla, index_col=0)
                df_old.drop(["Promedio"], inplace=True)

                df_aux = pd.DataFrame()
                df_aux["Localidad"] = df_old.shape[0] * ['']
                df_aux["Muestra"] = df_old.index
                df_aux["Unidad"] = df_old.shape[0] * ['']
                df_aux["Latitud"] = df_old.shape[0] * ['']
                df_aux["Longitud"] = df_old.shape[0] * ['']
                df_aux["Profundidad"] = df_old.shape[0] * ['']

                df_aux = df_aux.join(df_old, on='Muestra')
                df_old = df_aux.set_index(["Localidad", "Muestra", "Unidad"])
            else:
                df_old = pd.read_excel(self.nombre_tabla, index_col=[0, 1, 2])
                df_old.drop(index="Promedio", level=1, inplace=True)

            for clasificacion in nombre_clasificacion.values():
                if clasificacion in df_old.columns:
                    df_old.drop(columns=[clasificacion], inplace=True)

            df_new = pd.concat([df_old, df_new])
            df_new[columnas_rocas(df_new)] = df_new[columnas_rocas(df_new)].fillna(0)
        else:
            df_new[columnas_rocas(df_new)] = df_new[columnas_rocas(df_new)].fillna(0)

        # Calculo el promedio de cada columna
        promedio = df_new[columnas_rocas(df_new)].mean()
        # Asignar nada a las coordenadas y profundidad en el promedio
        promedio["Latitud"] = None
        promedio["Longitud"] = None
        promedio["Profundidad"] = None
        promedio["Localidad"] = None
        promedio["Muestra"] = "Promedio"
        promedio["Unidad"] = None
        df_promedio = pd.DataFrame(promedio).T.set_index(["Localidad", "Muestra", "Unidad"])
        df_new = pd.concat([df_new, df_promedio])

        def ordenar_columnas(columnas):
            Qs, Fs, Ls, Os = [], [], [], []
            for columna in sorted(columnas):
                if columna[1] == 'Q':
                    Qs.append(columna)
                elif columna[1] == 'F':
                    Fs.append(columna)
                elif columna[1] == 'L':
                    Ls.append(columna)
                elif columna[1] == 'O':
                    Os.append(columna)
            return Qs + Fs + Ls + Os

        df_new = df_new[["Latitud", "Longitud", "Profundidad"] + ordenar_columnas(df_new.columns)]
        df_new.to_excel(self.nombre_tabla, index_label=['Localidad', 'Muestra', 'Unidad'])

        return self.nombre_tabla

    def getComponentesCount(self) -> Dict[str, int]:
        d = dict(Counter(self.componentes))
        for nombres_rocas in self.mapa.values():
            if nombres_rocas not in d and nombres_rocas != '':
                d[nombres_rocas] = 0

        return d
