import os
from collections import Counter
from typing import Dict

import pandas as pd

from diagrama import nombre_clasificacion


class Muestra:
    def __init__(self, nombre, fecha, localidad, operador, cantidad_lecturas, observaciones, mapa, fileName):
        self.nombre = nombre
        self.fecha = fecha
        self.localidad = localidad
        self.operador = operador
        self.cantidad_lecturas = cantidad_lecturas
        self.observaciones = observaciones
        self.mapa = mapa
        self.fileName = fileName
        self.componentes = []

    def exportar_datos(self):
        path_dir = os.path.dirname(self.fileName)
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)

        df_new = pd.DataFrame(self.componentes, columns=["Muestra"])
        counts_df = pd.DataFrame(df_new["Muestra"].value_counts(normalize=True) * 100)
        df_new = counts_df.rename(columns={"proportion": self.nombre}).T
        df_new.rename(index={'Muestra': self.nombre}, inplace=True)

        # Cargar viejo Excel y concatenarlo
        file_path = os.path.join(path_dir, f"{self.localidad}.xlsx")
        if os.path.isfile(file_path):
            df_old = pd.read_excel(file_path, index_col=0)
            df_old.drop(["Promedio"], inplace=True)

            for clasificacion in nombre_clasificacion.values():
                if clasificacion in df_old.columns:
                    df_old.drop(columns=[clasificacion], inplace=True)

            df_new = pd.concat([df_old, df_new]).fillna(0)

        # Calculo el promedio de cada columna
        promedio = df_new.mean()
        promedio["Muestra"] = "Promedio"
        df_promedio = pd.DataFrame(promedio).T.set_index("Muestra")
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

        df_new = df_new[ordenar_columnas(df_new.columns)]

        mapa_fileName = os.path.join(path_dir, f"{self.localidad}.xlsx")
        df_new.to_excel(mapa_fileName, index_label='Muestra')
        return mapa_fileName

    def getComponentesCount(self) -> Dict[str, int]:
        d = dict(Counter(self.componentes))
        for nombres_rocas in self.mapa.values():
            if nombres_rocas not in d and nombres_rocas != '':
                d[nombres_rocas] = 0

        return d
