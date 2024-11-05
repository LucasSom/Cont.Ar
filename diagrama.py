from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.lines as mlines


nombre_clasificacion = {
    'Pettijohn_1977': "Pettijohn",
    'Dickinson_1983_QFL': "Dickinson_QFL",
    'Dickinson_1983_QmFLQp': "Dickinson_QmFLQp",
    'Garzanti_2019': 'Garzanti',
    'Folk': 'Folk'
}
y_axis_scale = 2 / (3 ** 0.5)


def data_prep(data, top, left, right):
    if type(top) == str:
        top = data[top]
        left = data[left]
        right = data[right]
    else:
        top = top
        left = left
        right = right

    stacked_data = np.vstack((top, left, right))
    summed_rows = np.sum(stacked_data[0:], axis=0)
    stacked_data = np.vstack((stacked_data, summed_rows))
    T = (stacked_data[0] / stacked_data[3] * 100)
    L = (stacked_data[1] / stacked_data[3] * 100)
    y = T / 100
    x = (1 - L / 100) - (y / 2)
    return x, y


def field_boundaries(scheme):
    classifications, labels = None, None
    if scheme == 'Pettijohn_1977':
        c1 = ['Quartz arenite', (0.5, 0.9), (0.525, 0.95), (0.5, 1), (0.475, 0.95), (0.5, 0.9)]
        c2 = ['Sublitharenite', (0.5, 0.5), (0.625, 0.75), (0.525, 0.95), (0.5, 0.9), (0.5, 0.5)]
        c3 = ['Lithic arenite', (1, 0), (0.625, 0.75), (0.5, 0.5), (0.5, 0.0), (1, 0)]
        c4 = ['Arkosic arenite', (0, 0), (0.375, 0.75), (0.5, 0.5), (0.5, 0.0), (0, 0)]
        c5 = ['Subarkose', (0.5, 0.5), (0.375, 0.75), (0.475, 0.95), (0.5, 0.9), (0.5, 0.5)]
        classifications = [c1, c2, c3, c4, c5]
        # label, x, y, rotation

        l1 = ["Quartz arenite", 0.62, 0.95, 0]
        l2 = ["Sublitharenite", 0.7, 0.8, 0]

        l3 = ["Lithic arenite", 0.75, 0.05, 0]
        l4 = ["Subarkose", 0.32, 0.83, 0]
        l5 = ["Arkosic arenite", 0.25, 0.05, 0]
        labels = [l1, l2, l3, l4, l5]
    elif scheme == 'Dickinson_1983_QFL':
        # c1 = ['basement uplift', (0, 0), (0.15, 0), (0.341992, 0.4985), (0.266412, 0.532842), (0, 0)]
        # c2 = ['transitional continental', (0.341992, 0.4985), (0.266412, 0.532842), (0.403822, 0.807654), (0.45, 0.779),
        #       (0.341992, 0.4985)]
        # c3 = ['craton interior', (0.45, 0.779), (0.403822, 0.807654), (0.5, 1), (0.52, 0.96), (0.45, 0.779)]
        # c4 = ['recycled orogen', (0.886, 0.228), (0.341992, 0.4985), (0.52, 0.96), (0.886, 0.228)]
        # c5 = ['dissected arcs', (0.341992, 0.4985), (0.701343, 0.319926), (0.215664, 0.170566),
        #       (0.341992, 0.4985)]
        # c6 = ['transitional arc', (0.701343, 0.319926), (0.863323, 0.239235), (0.5, 0), (0.15, 0),
        #       (0.215664, 0.170566),
        #       (0.701343, 0.319926)]
        # c7 = ['undissected arc', (0.863323, 0.239235), (0.886, 0.228), (1, 0), (0.5, 0), (0.863323, 0.2392359)]
        # classifications = [c1, c2, c3, c4, c5, c6, c7]
        # l1 = ["basement uplift", 0.165, 0.2, 58]
        # l2 = ["transitional\n continental", 0.365, 0.65, 60]
        # l3 = ["craton interior", 0.38, 0.92, 0]
        # l4 = ["recycled orogen", 0.54, 0.62, 0]
        # l5 = ["dissected arcs", 0.41, 0.35, 0]
        # l6 = ["transitional arc", 0.45, 0.15, 0]
        # l7 = ["undissected arc", 0.8, 0.05, 0]

        c1 = ['basamento elevado', (0, 0), (0.15, 0), (0.341992, 0.4985), (0.266412, 0.532842), (0, 0)]
        c2 = ['continental\ntransicional', (0.341992, 0.4985), (0.266412, 0.532842), (0.403822, 0.807654), (0.45, 0.779),
              (0.341992, 0.4985)]
        c3 = ['interior cratónico', (0.45, 0.779), (0.403822, 0.807654), (0.5, 1), (0.52, 0.96), (0.45, 0.779)]
        c4 = ['orógeno reciclado', (0.886, 0.228), (0.341992, 0.4985), (0.52, 0.96), (0.886, 0.228)]
        c5 = ['arco disectado', (0.341992, 0.4985), (0.701343, 0.319926), (0.215664, 0.170566),
              (0.341992, 0.4985)]
        c6 = ['arco transicional', (0.701343, 0.319926), (0.863323, 0.239235), (0.5, 0), (0.15, 0),
              (0.215664, 0.170566),
              (0.701343, 0.319926)]
        c7 = ['arco no disectado', (0.863323, 0.239235), (0.886, 0.228), (1, 0), (0.5, 0), (0.863323, 0.2392359)]
        classifications = [c1, c2, c3, c4, c5, c6, c7]

        l1 = ["basamento elevado", 0.165, 0.2, 58]
        l2 = ["continental\ntransicional", 0.365, 0.65, 60]
        l3 = ["interior cratónico", 0.38, 0.92, 0]
        l4 = ["orógeno reciclado", 0.54, 0.62, 0]
        l5 = ["arco disectado", 0.41, 0.35, 0]
        l6 = ["arco transicional", 0.45, 0.15, 0]
        l7 = ["arco no disectado", 0.8, 0.05, 0]
        labels = [l1, l2, l3, l4, l5, l6, l7]
    elif scheme == 'Dickinson_1983_QmFLQp':
        A = (0, 0)
        A1 = (0.7925, 0.1143 * y_axis_scale)
        B = (1, 0)
        B1 = (0.7473, 0.1809 * y_axis_scale)
        C = (0.5, 0.866025404 * y_axis_scale)
        C1 = (0.6976, 0.2541 * y_axis_scale)
        D = (0.23, 0)
        D1 = (0.6945, 0.2536 * y_axis_scale)
        E = (0.47, 0)
        E1 = (0.4078, 0.4216 * y_axis_scale)
        F = (0.87, 0)
        F1 = (0.4753, 0.5818 * y_axis_scale)
        G1 = (0.5789, 0.4291 * y_axis_scale)
        H1 = (0.7003, 0.2502 * y_axis_scale)
        I1 = (0.497, 0.6332 * y_axis_scale)
        J = (0.285, 0.4936 * y_axis_scale)
        L = (0.4, 0.6928 * y_axis_scale)
        Q = (0.855, 0.2511 * y_axis_scale)
        U = (0.71, 0.5023 * y_axis_scale)
        W = (0.555, 0.7708 * y_axis_scale)
        Z = (0.3108, 0.1916 * y_axis_scale)

        # c1 = ['basement uplift', A, D, E1, J, A]
        # c2 = ['transitional continental', E1, I1, L, J, E1]
        # c3 = ['craton interior', I1, W, C, L, I1]
        #
        # c4 = ['mixed', H1, F1, E1, H1]
        # c5 = ['dissected arcs', E1, D1, Z, E1]
        # c6 = ['transitional arc', D, E, A1, C1, Z, D]
        # c7 = ['undissected arc', E, F, A1, E]
        #
        # c8 = ['quartzose recycled', W, F1, G1, U, W]
        # c9 = ['transitional recycled', B1, Q, U, G1, B1]
        # c10 = ['lithic recycled', F, B, Q, B1, F]
        # classifications = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
        #
        # l1 = ["basement uplift", 0.165, 0.2, 58]
        # l2 = ["transitional\n continental", 0.4, 0.65, 60]
        # l3 = ["craton interior", 0.5, 0.93, 0]
        # l4 = ["mixed", 0.5, 0.5, 0]
        # l5 = ["dissected\narc", 0.46, 0.31, 0]
        # l6 = ["transitional\narc", 0.45, 0.15, 0]
        # l7 = ["undissected arc", 0.72, 0.025, 0]
        # l8 = ["quartzose\nrecycled", 0.6, 0.7, 300]
        # l9 = ["transitional\nrecycled", 0.7, 0.4, 300]
        # l10 = ["lithic recycled", 0.92, 0.15, 0]

        c1 = ['basamento elevado', A, D, E1, J, A]
        c2 = ['continental\ntransicional', E1, I1, L, J, E1]
        c3 = ['interior cratónico', I1, W, C, L, I1]

        c4 = ['mezcla', H1, F1, E1, H1]
        c5 = ['arco\ndisectado', E1, D1, Z, E1]
        c6 = ['arco\ntransicional', D, E, A1, C1, Z, D]
        c7 = ['arco no\ndisectado', E, F, A1, E]

        c8 = ['orógeno\nreciclado\ncuarzoso', W, F1, G1, U, W]
        c9 = ['orógeno\nreciclado\ntransicional', B1, Q, U, G1, B1]
        c10 = ['orógeno\nreciclado\nlítico', F, B, Q, B1, F]
        classifications = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]

        l1 = ["basamento elevado", 0.165, 0.2, 58]
        l2 = ["continental\ntransicional", 0.4, 0.65, 60]
        l3 = ["interior cratónico", 0.5, 0.93, 0]
        l4 = ["mezcla", 0.5, 0.5, 0]
        l5 = ["arco\ndisectado", 0.46, 0.31, 0]
        l6 = ["arco\ntransicional", 0.45, 0.15, 0]
        l7 = ["arco no\ndisectado", 0.72, 0.05, 0]
        l8 = ["orógeno\nreciclado\ncuarzoso", 0.58, 0.65, 300]
        l9 = ["orógeno\nreciclado\ntransicional", 0.72, 0.4, 300]
        l10 = ["orógeno\nreciclado\nlítico", 0.87, 0.15, 0]

        labels = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]

    elif scheme == 'Garzanti_2019':
        A = (0, 0)
        B = (1, 0)
        C = (0.5, 0.866025404 * y_axis_scale)
        D = (0.1, 0)
        E = (0.05, 0.09 * y_axis_scale)
        F = (0.9, 0)
        G = (0.95, 0.09 * y_axis_scale)
        H = (0.5, 0)
        I = (0.45, 0.78 * y_axis_scale)
        J = (0.55, 0.78 * y_axis_scale)
        K = (0.25, 0.43 * y_axis_scale)
        L = (0.75, 0.43 * y_axis_scale)
        M = (0.5, 0.29 * y_axis_scale)
        N = (0.15, 0.09 * y_axis_scale)
        O = (0.85, 0.09 * y_axis_scale)
        P = (0.5, 0.69 * y_axis_scale)
        Q = (0.33, 0.39 * y_axis_scale)
        R = (0.68, 0.39 * y_axis_scale)
        S = (0.5, 0.09 * y_axis_scale)

        c1 = ['feldespática', A, D, N, E, A]
        c2 = ['cuarzosa', C, I, P, J, C]
        c3 = ['lítica', B, G, O, F, B]

        c4 = ['feldespática-cuarzosa', E, N, Q, K, E]
        c5 = ['cuarzo-feldespática', K, Q, P, I, K]
        c6 = ['cuarzo-lítica', P, J, L, R, P]
        c7 = ['lítica-cuarzosa', R, L, G, O, R]
        c8 = ['', D, N, S, H, D]
        c9 = ['lito-feldespática', O, F, H, S, O]

        c10 = ['IQF', M, N, Q, M]
        c11 = ['IFQ', M, P, Q, M]
        c12 = ['fLQ', M, R, P, M]
        c13 = ['fQL', M, R, O, M]
        c14 = ['qFL', M, O, S, M]
        c15 = ['qLF', M, S, N, M]
        classifications = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15]

        l1 = ["feldespática", 0.05, 0.05, 0]
        l2 = ["cuarzosa", 0.5, 0.92, 0]
        l3 = ["lítica", 0.92, 0.05, 0]
        l4 = ["feldespática-cuarzosa", 0.2, 0.3, 55]
        l5 = ["cuarzo-feldespática", 0.38, 0.65, 55]
        l6 = ["cuarzo-lítica", 0.6, 0.7, 305]
        l7 = ["lítica-cuarzosa", 0.8, 0.3, 305]
        l8 = ["feldespato-lítica", 0.3, 0.05, 0]
        l9 = ["lito-feldespática", 0.7, 0.05, 0]
        l10 = ["IQF", 0.32, 0.35, 0]
        l11 = ["IFQ", 0.43, 0.5, 0]
        l12 = ["fLQ", 0.57, 0.5, 0]
        l13 = ["fQL", 0.67, 0.35, 0]
        l14 = ["qFL", 0.6, 0.15, 0]
        l15 = ["qLF", 0.4, 0.15, 0]

        labels = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15]

    elif scheme == 'Folk':
        A = (0, 0)
        B = (1, 0)
        C = (0.5, 0.866025404 * y_axis_scale)
        E = (0.53, 0.82 * y_axis_scale)
        G = (0.475, 0.82 * y_axis_scale)
        H = (0.75, 0)
        I = (0.375, 0.65 * y_axis_scale)
        J = (0.25, 0)
        K = (0.63, 0.65 * y_axis_scale)
        L = (0.5, 0.65 * y_axis_scale)
        M = (0.5, 0)
        N = (0.5, 0.82 * y_axis_scale)
        O = (0.44, 0.65 * y_axis_scale)
        P = (0.56, 0.65 * y_axis_scale)

        c1 = ['cuarzoarenita', C, G, E, C]

        c2 = ['subfeldarenita', G, N, L, I, G]
        c3 = ['sublitoarenita', N, E, K, L, N]

        c4 = ['feldarenita', A, J, O, I, A]
        c5 = ['feldarenita lítica', J, O, L, M, J]
        c6 = ['litoarenita feldespática', M, L, P, H, M]
        c7 = ['litoarenita', H, P, K, B, H]

        classifications = [c1, c2, c3, c4, c5, c6, c7]

        l1 = ["cuarzoarenita", 0.5, 1, 0]

        l2 = ["subfeldarenita", 0.3, 0.85, 0]
        l3 = ["sublitoarenita", 0.7, 0.85, 0]

        l4 = ["feldarenita", 0.2, 0.3, 60]
        l5 = ["feldarenita lítica", 0.4, 0.3, 80]
        l6 = ["litoarenita feldespática", 0.6, 0.3, 280]
        l7 = ["litoarenita", 0.8, 0.3, 300]

        labels = [l1, l2, l3, l4, l5, l6, l7]

    elif scheme == 'blank':
        c1 = ['triangle', (0, 0), (0.5, 1), (1, 0), (0, 0)]
        classifications = [c1]
        labels = []

    return classifications, labels


def plot_diagrama(data, top, left, right, matrix=None, plot_type='blank', top_label='', left_label='', right_label='',
                  grid=True, color='g', size=15, include_last_row=True) -> Tuple[pd.DataFrame, plt.Figure]:
    """
    Grafica un diagrama triangular. Para QFL top=cuarzo, left=feldespato, right=lítico.

    :param data: Pandas data frame conteniendo los datos a los cuales las clasificaciones serán agregadas
    :param top: str o array. Comúnmente serán arrays de 1D pero pueden ser strings referenciando las columnas del
     dataframe. Para QFL top=cuarzo.
    :param left: str o array. Ídem 'top'. Para QFL left=feldespato.
    :param right: str o array. Ídem 'top'. Para QFL right=lítico.
    :param matrix: str or array-like, optional, default=None. Si se grafican datos petrográficos pueden incluirse en
     este parámetro los clay matrix. Estructura análoga a los anteriores.
    :param plot_type: Tipo de gráfico. Son 3 opciones: 'Pettijohn_1977', 'Dickinson_1983_QFL', 'Dickinson_1983_QmFLQp',
     'Garzanti_2019', 'Folk' o 'blank'. Default: 'blank'
    :param top_label: Label del vértice superior del triángulo (para QFL, 'Q').
    :param left_label: Label del vértice izquierdo del triángulo (para QFL, 'F').
    :param right_label: Label del vértice derecho del triángulo (para QFL, 'L').
    :param grid: Bool que indica si se dibuja la grilla en el triángulo o no. Default: 'True'
    :param color: Color de los puntos a marcar. Default: 'r'
    :param size: Tamaño de la marca. Default: '15'
    :param include_last_row: Si se incluye la última fila del data frame (típicamente el promedio)
    :return: tupla con el Dataframe de entrada al que se le agrega una columna con el valor de la clasificación según
     el plot_type elegido
    """
    list_valid_types = ['Pettijohn_1977', 'Dickinson_1983_QFL', 'Dickinson_1983_QmFLQp', 'Garzanti_2019', 'Folk', 'blank']
    if plot_type not in list_valid_types:
        raise ValueError("Plot type not recognised, valid types are 'blank', 'Pettijohn_1977', 'Dickinson_1983_QFL', "
                         "'Dickinson_1983_QmFLQp', 'Garzanti_2019' and 'Folk'")

    x, y = data_prep(data, top, left, right)
    fig, ax = plt.subplots()
    classifications, labs = field_boundaries(plot_type)

    for lab in labs:
        ax.text(lab[1], lab[2], lab[0], ha="center", va="center", rotation=lab[3], size=8)

    ax.scatter(x[:-1], y[:-1], color=color, s=size, edgecolor='k', zorder=10)
    if include_last_row:
        ax.scatter(x[-1], y[-1], color='r', s=size+1, edgecolor='k', zorder=10)
    for i, muestra in enumerate(data.index):
        if i < len(data.index) - 1 or include_last_row:
            plt.text(x[i] * (1 + 0.01), y[i] * (1 + 0.01), muestra, fontsize=8)
    ax.set_frame_on(False)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    # label the apexes of the triangle
    ax.text(-0.02, -0.04, str(left_label), ha="center", va="center", rotation=0, size=12)
    ax.text(1.02, -0.04, str(right_label), ha="center", va="center", rotation=0, size=12)
    ax.text(0.5, 1.05, str(top_label), ha="center", va="center", rotation=0, size=12, zorder=0)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)

    if grid:
        grid1 = np.linspace(0.1, 0.9, 9)
        grid2 = np.linspace(0.05, .45, 9)
        axislabels = list(range(10, 100, 10))
        for g1, g2, axlab in zip(grid1, grid2, axislabels):
            l0 = mlines.Line2D([g2, 1 - g2], [g1, g1], linestyle=':', linewidth=0.5, zorder=0, color='k')
            l1 = mlines.Line2D([g1, g2], [0, g1], linestyle=':', linewidth=0.5, zorder=0, color='k')
            l2 = mlines.Line2D([1 - g1, 1 - g2], [0, g1], linestyle=':', linewidth=0.5, zorder=0, color='k')
            ax.text(g1, -0.02, axlab, ha="center", va="center", rotation=0, size=5)
            ax.text(1.02 - g2, g1, axlab, ha="center", va="center", rotation=0, size=5)
            ax.text(0.48 - g2, 1 - g1, axlab, ha="center", va="center", rotation=0, size=5)
            ax.add_line(l0)
            ax.add_line(l1)
            ax.add_line(l2)

        grid1 = np.linspace(0.1, 0.9, 9)
        grid2 = np.linspace(0.05, .45, 9)
        axislabels = list(range(10, 100, 10))
        for g1, g2, axlab in zip(grid1, grid2, axislabels):
            l0 = mlines.Line2D([g2, 1 - g2], [g1, g1], linestyle=':', linewidth=0.5, zorder=0, color='k')
            l1 = mlines.Line2D([g1, g2], [0, g1], linestyle=':', linewidth=0.5, zorder=0, color='k')
            l2 = mlines.Line2D([1 - g1, 1 - g2], [0, g1], linestyle=':', linewidth=0.5, zorder=0, color='k')
            ax.text(g1, -0.02, axlab, ha="center", va="center", rotation=0, size=5)
            ax.text(1.02 - g2, g1, axlab, ha="center", va="center", rotation=0, size=5)
            ax.text(0.48 - g2, 1 - g1, axlab, ha="center", va="center", rotation=0, size=5)
            ax.add_line(l0)
            ax.add_line(l1)
            ax.add_line(l2)

    # add the fields for each petrographic classification
    for classification in classifications:
        polygon = classification[1:]
        path = Path(polygon)
        # check if every polygon in the loop contains points and color green if true
        index = path.contains_points(np.column_stack((x, y)))
        if plot_type != 'blank':
            if sum(index) > 0:
                ax.add_patch(patches.PathPatch(path, alpha=0.1, facecolor='green', lw=0, zorder=0))
        patch = patches.PathPatch(path, color=None, facecolor=None, fill=False, lw=1.5, zorder=1)
        ax.add_patch(patch)

    if plot_type != 'blank':
        final_data = data.copy()
        for classification in classifications:
            polygon = classification[1:]
            path = Path(polygon)
            # check if points are within each polygon
            # the radius argument allows samples plotting on boundary to be classified
            index = path.contains_points(np.column_stack((x, y)), radius=-0.01)
            index1 = path.contains_points(np.column_stack((x, y)), radius=0.01)
            for j in range(len(index)):
                if index[j] or index1[j]:
                    final_data.loc[final_data.index[j], nombre_clasificacion[plot_type]] = classification[0]
                    # add the classification to the column nombre_clasificacion in the datatable

                    if matrix is not None:
                        if 15 < matrix[j] < 75:  # change the classification if matrix > 15% and less <75%
                            if classification[0] == 'Sublith Arenite' or classification[0] == 'Lith Arenite':
                                final_data.loc[j, "Clasificación"] = 'Lithic Wacke'
                            elif classification[0] == 'Sub Arkose' or classification[0] == 'Arkosic Arenite':
                                final_data.loc[j, "Clasificación"] = 'Arkosic Wacke'
                            elif classification[0] == 'Quartz Arenite':
                                final_data.loc[j, "Clasificación"] = 'Quartz Wacke'
                        elif matrix[j] > 75:
                            final_data.loc[j, "Clasificación"] = 'Mudrock'

        return final_data, fig

    return data.set_index('Muestra') if data.index.name != 'Muestra' else data, fig


if __name__ == "__main__":
    data = pd.read_csv('data.csv')
    print(data.columns.values)
    data_pct = data.set_index('Classification')
    # convert counts to percent
    data_pct = data_pct.div(data_pct.sum(axis=1), axis=0) * 100
    # sum quartz types
    quartz = data_pct['Qm'] + data_pct['Qmu'] + data_pct['Qp']
    fsp = data_pct['Plag'] + data_pct['Afsp']
    lithic = data_pct['Lf']
    # the clay matrix can be None if not present
    matrix = data_pct['PM+Cem']
    # for QFL top = quzrtz, left = feldspar, right = lithic
    # plot type options are 'Dickinson_1983', 'Pettijohn_1977' or 'blank'
    classified_data, plot = plot_diagrama(data, top=quartz, left=fsp, right=lithic, matrix=matrix, plot_type='Pettijohn_1977',
                                          top_label='Q', left_label='F', right_label='L', grid=True, color='r', size=15)
    plt.show()
    print(classified_data)
