import pandas as pd
import plotly.express as px

#aquí cargar los datos
df = pd.read_csv("  ")

df_jalisco = df[df['ent_ocurr'] == 14]

df_jalisco['edad_madn'] = pd.to_numeric(df_jalisco['edad_madn'], errors='coerce')
df_jalisco['edad_padn'] = pd.to_numeric(df_jalisco['edad_padn'], errors='coerce')
df_jalisco['hijos_vivo'] = pd.to_numeric(df_jalisco['hijos_vivo'], errors='coerce')


df_jalisco['edad_madn_cat'] = pd.cut(df_jalisco['edad_madn'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])
df_jalisco['edad_padn_cat'] = pd.cut(df_jalisco['edad_padn'], bins=[0, 20, 30, 40, 50, 60, 100], labels=['0-20', '21-30', '31-40', '41-50', '51-60', '60+'])


df_jalisco['info'] = (
    'Edad de la Madre: ' + df_jalisco['edad_madn'].astype(str) + '<br>' +
    'Edad del Padre: ' + df_jalisco['edad_padn'].astype(str) + '<br>' +
    'Hijos Vivos: ' + df_jalisco['hijos_vivo'].astype(str)
)


fig = px.density_heatmap(
    df_jalisco,
    x='edad_madn_cat',
    y='edad_padn_cat',
    z='hijos_vivo',
    hover_name='info',
    labels={'edad_madn_cat': 'Edad de la Madre', 'edad_padn_cat': 'Edad del Padre', 'hijos_vivo': 'Hijos Vivos'},
    color_continuous_scale="Viridis",
)

fig.update_layout(
    title="Mapa de calor Jalisco",
    xaxis_title="Edad de la Madre",
    yaxis_title="Edad del Padre",
)


fig.show()
