import numpy as np
import pandas as pd


# -----------------------------
# Calcular distancia de Haversine (km)
# -----------------------------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0088
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


# -----------------------------
# Calcular atractivo turístico (por inmueble)
# -----------------------------
def tourist_score_0_100 (lat, lon, poi_df, sigma_km=1.5, weight_col="weight"):
    """
    Índice turístico más equilibrado [0,100]
    usando decaimiento exponencial en lugar de corte duro.
    """

    d_km = haversine_km(lat, lon, poi_df["lat"].to_numpy(), poi_df["lon"].to_numpy())

    # Mejor que corte duro
    prox = np.exp(-d_km / sigma_km)

    w = poi_df[weight_col].to_numpy().astype(float)
    w_sum = w.sum()

    if w_sum == 0:
        return 0.0

    score_0_1 = (w * prox).sum() / w_sum

    return float(score_0_1 * 100.0)


# ---------------------------------------------------
# Mapa de calor del atractivo turístico en Madrid
# ---------------------------------------------------
def tourist_score_map(df, output_html="tourist_score_map.html"):
    """
    Genera y guarda un mapa de calor de atractivo turístico en Madrid.
    df: DataFrame con columnas 'latitude', 'longitude', 'tourist_score'.
    output_html: nombre del archivo HTML de salida.
    """
    import folium
    from folium.plugins import HeatMap

    madrid_coords = [40.4168, -3.7038]
    m = folium.Map(location=madrid_coords, zoom_start=12)

    heat_data = (
    df[["latitude", "longitude", "tourist_score"]]
    .dropna()
    .values
    .tolist()
)
    HeatMap(
        heat_data,
        radius=12,
        blur=15,
        min_opacity=0.4,
        max_opacity=0.8,
        gradient={0.2: "blue", 0.5: "lime", 0.8: "red"},
    ).add_to(m)

    m.save(output_html)
    return output_html

#Estandarización de variables al importar
import unicodedata
import re

def estandarizar_columnas(df):
    columnas_limpias = []
    for col in df.columns:
        # 1. Convertir a minúsculas
        col = col.lower()
        # 2. Normalizar tildes (quitar acentos)
        col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('utf-8')
        # 3. Reemplazar caracteres especiales largos (como guion largo –) por _
        col = col.replace('–', '_')
        # 4. Reemplazar espacios por _
        col = col.replace(' ', '_')
        # 5. Reemplazar cualquier carácter no alfanumérico (excepto _ y %) por _
        col = re.sub(r'[^\w%]', '_', col)
        # 6. Reemplazar múltiples _ seguidos por uno solo
        col = re.sub(r'__+', '_', col)
        # 7. Eliminar _ al final/inicio si existen
        col = col.strip('_')
        columnas_limpias.append(col)
    df.columns = columnas_limpias
    return df

def estimate_gross_margin(
    df,
    district,
    neighbourhood,
    bedrooms,
    beds,
    accommodates,
    room_type,
    percentiles=[0.5, 0.75, 0.90, 0.95, 0.99]
):
    """
    Estimate gross margin potential for a specific property configuration.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset containing property information and gross margin.
    district : str
        District where the property is located.
    neighbourhood : str
        Neighbourhood where the property is located.
    bedrooms : int
        Number of bedrooms.
    beds : list
        Number of possible beds.
    accommodates : int
        Maximum number of guests.
    room_type : str
        Type of property.
    percentiles : list, optional
        Percentiles used to estimate gross margin potential.

    Returns
    -------
    pandas.Series
        Gross margin thresholds for the selected percentiles.
    """

    properties = df[
        (df["neighbourhood_group"] == district) &
        (df["neighbourhood"] == neighbourhood) &
        (df["bedrooms"] == bedrooms) &
        (df["beds"].isin(beds)) &
        (df["accommodates"] <= accommodates) &
        (df["room_type"] == room_type)
    ]

    print(f"District: {district}")
    print(f"Neighbourhood: {neighbourhood}")
    print(f"Configuration: {bedrooms} bedrooms, {beds} beds, "
          f"{accommodates} maximum accommodates, {room_type}")

    if properties.empty:
        print("No properties found for this configuration.")
        return None

    print(f"Properties: {len(properties)}")

    thresholds = properties["gross_margin"].quantile(percentiles)
     
    for percentile, threshold in thresholds.items():

        property_count = len(properties[properties["gross_margin"].ge(properties["gross_margin"].quantile(percentile))])

        print(
            f"{int(percentile * 100)} percentile: "
            f"{threshold:.2f}% gross margin"
            f" | Properties: {property_count})"
        )