import pandas as pd
from PyQt5.QtWidgets import QMainWindow
from matplotlib import pyplot as plt

from GUI.graficos.generar_graficos_ui import Ui_GraficosWindow
from diagrama import plot_diagrama, nombre_clasificacion
from utils import filtrar_tipo_roca, error_window, info_window


class GraficosWindow(QMainWindow, Ui_GraficosWindow):
    def __init__(self, df, file_name):
        QMainWindow.__init__(self)
        self.relacion_window = None
        self.file_name = file_name
        self.df = df
        self.incluir_promedio = False
        self.setupUi(self)

        self.QFL_boton_dickinson.clicked.connect(self.generar_qfl_dickinson)
        self.QFL_boton_folk.clicked.connect(self.generar_qfl_folk)
        self.QFL_boton_garzanti.clicked.connect(self.generar_qfl_garzanti)
        self.QmFLQp_boton.clicked.connect(self.generar_QmFLQp)
        # self.relacion_Fp_F_Boton.clicked.connect(self.relacion_Fp_F)
        self.LVLSLm_boton.clicked.connect(self.generar_LvLsLm)
        self.checkBox_promedio.toggled.connect(self.invertir_promedio)

    def invertir_promedio(self):
        self.incluir_promedio = not self.incluir_promedio

    def generar_qfl_dickinson(self):
        self.generar_qfl(clasificacion='Dickinson_1983_QFL')

    def generar_qfl_folk(self):
        self.generar_qfl(clasificacion='Folk')

    def generar_qfl_garzanti(self):
        self.generar_qfl(clasificacion='Garzanti_2019')

    def generar_qfl(self, clasificacion):
        try:
            cuarzos = filtrar_tipo_roca(self.df, tipo='Q')
            feldespatos = filtrar_tipo_roca(self.df, tipo='F')
            liticos = filtrar_tipo_roca(self.df, tipo='L')
            # the clay matrix can be None if not present
            otros = filtrar_tipo_roca(self.df, tipo='O')

            classified_data, plot = plot_diagrama(self.df,
                                                  top=cuarzos, left=feldespatos,
                                                  right=liticos, matrix=otros,
                                                  plot_type=clasificacion,
                                                  top_label='Q', left_label='F', right_label='L',
                                                  include_last_row=self.incluir_promedio)
            plot.show()
            self.df[nombre_clasificacion[clasificacion]] = classified_data[nombre_clasificacion[clasificacion]]
            self.df.to_excel(f"{self.file_name}.xlsx")

            df_reescalado = pd.DataFrame({
                'Q': cuarzos,
                'F': feldespatos,
                'L': liticos,
            }, index=self.df.index)

            sumatoria = df_reescalado.sum(axis=1)
            df_reescalado['Q'] = df_reescalado['Q'] / sumatoria * 100
            df_reescalado['F'] = df_reescalado['F'] / sumatoria * 100
            df_reescalado['L'] = df_reescalado['L'] / sumatoria * 100

            df_reescalado[f"Total-{clasificacion}"] = df_reescalado.sum(axis=1)
            export_path = f"{self.file_name}-QFL.xlsx"
            df_reescalado.to_excel(export_path)

            info_window(self, f"Tabla guardada en {export_path}")
        except Exception as e:
            error_window(self, e)

    def generar_QmFLQp(self):
        try:
            cuarzos_monocristalinos = filtrar_tipo_roca(self.df, tipo='Qm')
            feldespatos = filtrar_tipo_roca(self.df, tipo='F')
            liticos = filtrar_tipo_roca(self.df, tipo='L')
            cuarzos_policristalinos = filtrar_tipo_roca(self.df, tipo='Qp')

            classified_data, plot = plot_diagrama(self.df,
                                                  top=cuarzos_monocristalinos,
                                                  left=feldespatos,
                                                  right=liticos + cuarzos_policristalinos,
                                                  matrix=None,
                                                  plot_type='Dickinson_1983_QmFLQp',
                                                  top_label='Qm', left_label='F', right_label='L+Qp',
                                                  include_last_row=self.incluir_promedio)
            plot.show()
            self.df["Dickinson_QmFLQp"] = classified_data["Dickinson_QmFLQp"]
            self.df.to_excel(f"{self.file_name}.xlsx")

            df_reescalado = pd.DataFrame({
                'Qm': cuarzos_monocristalinos,
                'F': feldespatos,
                'L+Qp': liticos + cuarzos_policristalinos,
            }, index=self.df.index)

            sumatoria = df_reescalado.sum(axis=1)
            df_reescalado['Qm'] = df_reescalado['Qm'] / sumatoria * 100
            df_reescalado['F'] = df_reescalado['F'] / sumatoria * 100
            df_reescalado['L+Qp'] = df_reescalado['L+Qp'] / sumatoria * 100

            df_reescalado[f"Total-QmFLQp"] = df_reescalado.sum(axis=1)

            df_reescalado.index = self.df.index
            export_path = f"{self.file_name}-QmFLQp.xlsx"
            df_reescalado.to_excel(export_path)

            info_window(self, f"Tabla guardada en {export_path}")
        except Exception as e:
            error_window(self, e)

    def relacion_Fp_F(self):
        try:
            Fp = filtrar_tipo_roca(self.df, tipo='Fp')
            Fk = filtrar_tipo_roca(self.df, tipo='Fk')
            Fm = filtrar_tipo_roca(self.df, tipo='Fm')

            df_relacion = pd.DataFrame({'Fp': Fp, 'Fk': Fk, 'Fm': Fm})
            df_relacion['relacion_Fp_F'] = (Fp / (Fp + Fk + Fm)).fillna(0)
            if df_relacion.index.name != 'Muestra':
                df_relacion.set_index('Muestra', inplace=True)

            export_path = f"{self.file_name}-Fp_F.xlsx"
            df_relacion.to_excel(export_path)

            info_window(self, f"Tabla guardada en {export_path}")
        except Exception as e:
            error_window(self, e)

    def generar_LvLsLm(self):
        try:
            liticos_volcanicos = filtrar_tipo_roca(self.df, tipo='Lv')
            liticos_sedimentarios = filtrar_tipo_roca(self.df, tipo='Ls')
            liticos_metamorficos = filtrar_tipo_roca(self.df, tipo='Lm')

            classified_data, plot = plot_diagrama(self.df,
                                                  top=liticos_volcanicos,
                                                  left=liticos_sedimentarios,
                                                  right=liticos_metamorficos,
                                                  plot_type='blank',
                                                  top_label='Lv', left_label='Ls', right_label='Lm',
                                                  include_last_row=self.incluir_promedio)
            plot.show()

            df_reescalado = pd.DataFrame({
                'Lv': liticos_volcanicos,
                'Ls': liticos_sedimentarios,
                'Lm': liticos_metamorficos,
            }, index=self.df.index)

            sumatoria = df_reescalado.sum(axis=1)
            df_reescalado['Lv'] = df_reescalado['Lv'] / sumatoria * 100
            df_reescalado['Ls'] = df_reescalado['Ls'] / sumatoria * 100
            df_reescalado['Lm'] = df_reescalado['Lm'] / sumatoria * 100

            df_reescalado[f"Total-LvLsLm"] = df_reescalado.sum(axis=1)

            if df_reescalado.index.nlevels == 1 and df_reescalado.index.name != 'Muestra':
                df_reescalado.set_index('Muestra', inplace=True)
            export_path = f"{self.file_name}-LvLsLm.xlsx"
            df_reescalado.to_excel(export_path)

            info_window(self, f"Tabla guardada en {export_path}")

        except Exception as e:
            error_window(self, e)
