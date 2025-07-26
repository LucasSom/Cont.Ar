import pandas as pd
import simplekml

from utils.utils import nombre_clasificacion, warning_window


def exportar_kml(data, path, parent):
    # Crear objeto KML
    kml = simplekml.Kml()

    # Recorrer cada fila y agregar un punto al KML
    sin_coordenadas = False
    for _, row in data.iterrows():
        if pd.isna(row["Latitud"]) or pd.isna(row["Longitud"]):
            if row['Muestra'] != 'Promedio'  and not sin_coordenadas:
                warning_window(parent, f"Hay muestras sin coordenadas geográficas.\n"
                                       f"Se saltarán en el archivo KML.")
                sin_coordenadas = True
        else:
            punto = kml.newpoint(name=row["Muestra"],
                                 coords=[(row["Longitud"], row["Latitud"])],
                                 )
            punto.extendeddata.newdata(name="Localidad", value=row["Localidad"])
            punto.extendeddata.newdata(name="Unidad", value=row["Unidad"])
            if "Profundidad" in row and not pd.isna(row["Profundidad"]):
                punto.extendeddata.newdata(name="Profundidad", value=f"{int(row["Profundidad"])}m")
            for clasificacion in nombre_clasificacion.values():
                if clasificacion in row and not pd.isna(row[clasificacion]):
                    punto.extendeddata.newdata(name=clasificacion, value=row[clasificacion])



    # Guardar como archivo KML
    kml.save(f"{path}.kml")

    # También lo puedo guardar como un KMZ
    kml.savekmz(f"{path}.kmz")

    print("Archivo KML y KMZ exportados exitosamente.")

