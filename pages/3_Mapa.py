import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from branca.colormap import LinearColormap
from streamlit_option_menu import option_menu

st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Menú", 
        ["Inicio", "Dashboard", "Mapa"],  
        icons=["house", "bar-chart", "geo-alt"],  
        menu_icon="cast", 
        default_index=2
    )

if selected == "Inicio":
    st.switch_page("pages/1_Inicio.py")
elif selected == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")
else:
    

    st.set_page_config(page_title="Mapa Visitantes", layout="wide", initial_sidebar_state="collapsed")
    st.title("Mapa Interactivo de Visitantes")


    #Cargar datos
    data = pd.read_csv("data/turismo_nacional.csv")

    #Agrupar y calcular promedio de visitantes
    data = data.groupby(['Departamento', 'Destino', 'Temporada', 'Latitud', 'Longitud'])['Visitantes'].mean().reset_index()

    #Dropdowns para filtrar
    destinos = data["Destino"].unique()
    temporadas = data["Temporada"].unique()

    destino_sel = st.selectbox("Selecciona un destino", destinos)
    temporada_sel = st.selectbox("Selecciona una temporada", temporadas)

    #Filtrar según selección
    data_filtrado = data[
        (data["Destino"] == destino_sel) &
        (data["Temporada"] == temporada_sel)
    ]

    #Crear mapa
    m = folium.Map(location=[4.6097, -74.0818], zoom_start=5)

    #Crear escala de colores
    min_val, max_val = data_filtrado['Visitantes'].min(), data_filtrado['Visitantes'].max()
    colormap = LinearColormap(colors=["green", "yellow", "red"], vmin=min_val, vmax=max_val)

    #Añadir círculos al mapa
    for _, row in data_filtrado.iterrows():
        folium.CircleMarker(
            location=[row['Latitud'], row['Longitud']],
            radius=row['Visitantes'] / 500,  # escala ajustable según valores
            color=colormap(row['Visitantes']),
            fill=True,
            fill_color=colormap(row['Visitantes']),
            fill_opacity=0.7,
            popup=f"{row['Departamento']}<br>Visitantes: {row['Visitantes']:.0f}"
        ).add_to(m)

    #Añadir leyenda
    colormap.caption = f"Visitantes ({destino_sel} - {temporada_sel})"
    colormap.add_to(m)

    # Mostrar mapa
    st_folium(m, width=900, height=600)
    st.caption("Mapa de símbolos proporcionales con respecto al destino y temporada seleccionado")
