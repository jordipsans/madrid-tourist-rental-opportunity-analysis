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
def atractivo_turistico_0_100(lat, lon, poi_df, r_max_km=1.0, weight_col="weight"):
    """
    Devuelve índice [0,100] lineal según proximidad a POIs.
    0 = a >= Rmax de todos los POIs; 100 = encima de todos los POIs.
    """
    # Distancias a todos los POI
    d_km = haversine_km(
        lat, lon, poi_df["lat"].to_numpy(), poi_df["lon"].to_numpy()
    )  # shape (M,)

    # Proximidad lineal con recorte por Rmax
    d_clip = np.minimum(d_km, r_max_km)
    prox = (r_max_km - d_clip) / r_max_km  # en [0,1]

    # Ponderación
    w = poi_df[weight_col].to_numpy().astype(float)
    w_sum = w.sum()
    if w_sum == 0:
        return 0.0  # si no hay pesos/POIs, no hay atractivo

    score_0_1 = (w * prox).sum() / w_sum
    return float(score_0_1 * 100.0)


# ---------------------------------------------------
# Mapa de calor del atractivo turístico en Madrid
# ---------------------------------------------------
def mapa_atractivo_turistico(df, output_html="mapa_atractivo_turistico.html"):
    """
    Genera y guarda un mapa de calor de atractivo turístico en Madrid.
    df: DataFrame con columnas 'latitude', 'longitude', 'atractivo_turistico'.
    output_html: nombre del archivo HTML de salida.
    """
    import folium
    from folium.plugins import HeatMap

    madrid_coords = [40.4168, -3.7038]
    m = folium.Map(location=madrid_coords, zoom_start=12)

    heat_data = (
        df[["latitude", "longitude", "atractivo_turistico"]].dropna().values.tolist()
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
