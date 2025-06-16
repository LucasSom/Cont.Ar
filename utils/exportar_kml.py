import pandas as pd
import simplekml

from utils.utils import nombre_clasificacion, warning_window


def exportar_kml(data, path, parent):
    # Crear objeto KML
    kml = simplekml.Kml()

    # Recorrer cada fila y agregar un punto al KML
    for _, row in data.iterrows():
        if pd.isna(row["Latitud"]) or pd.isna(row["Longitud"]):
            if row['Muestra'] != 'Promedio':
                warning_window(parent, f"Coordenadas geográficas no encontradas para la muestra {row['Muestra']}.\n"
                                 f"Se saltará esta muestra en el archivo KML.")
        else:
            descripcion = f'Localidad: {row["Localidad"]}\nUnidad: {row["Unidad"]}'
            if "Profundidad" in row and not pd.isna(row["Profundidad"]):
                descripcion += f'\nProfundidad: {row["Profundidad"]}m'
            for clasificacion in nombre_clasificacion.values():
                if clasificacion in row and not pd.isna(row[clasificacion]):
                    descripcion += f'\n{clasificacion}: {row[clasificacion]}'

            kml.newpoint(name=row["Muestra"],
                         coords=[(row["Longitud"], row["Latitud"])],
                         description=descripcion,
                         )

    # Guardar como archivo KML
    kml.save(f"{path}.kml")

    # También lo puedo guardar como un KMZ
    kml.savekmz(f"{path}.kmz")

    print("Archivo KML y KMZ exportados exitosamente.")

