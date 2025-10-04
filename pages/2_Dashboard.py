import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
import plotly.express as px


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
        default_index=1  
    )

if selected == "Inicio":
    st.switch_page("pages/1_Inicio.py")
elif selected == "Mapa":
    st.switch_page("pages/3_Mapa.py")
else:
    st.set_page_config(page_title="Dashboard", layout="wide", initial_sidebar_state="collapsed")

    #Cargar datos
    data = pd.read_csv("data/turismo_nacional.csv")
    data_grouped = data.groupby(['Departamento', 'Destino', 'Temporada'])['Visitantes'].mean().reset_index()  

    #Métricas principales
    st.title("Estadísticas generales")

    col1, col2 = st.columns(2)
    col1.metric("Departamentos únicos", data_grouped['Departamento'].nunique())
    col2.metric("Destinos únicos", data_grouped['Destino'].nunique())

    #Estadísticas
    media_visitantes = data_grouped['Visitantes'].mean()
    max_visitantes = data_grouped['Visitantes'].max()
    min_visitantes = data_grouped['Visitantes'].min()

    col4, col5, col6 = st.columns(3)
    col4.metric("Media de visitantes", f"{media_visitantes:.0f}")
    col5.metric("Máximo visitantes", f"{max_visitantes:.0f}")
    col6.metric("Mínimo visitantes", f"{min_visitantes:.0f}")

    #Dropdowns
    departamentos = data_grouped["Departamento"].unique()
    temporadas = data_grouped["Temporada"].unique()
    destinos = data_grouped["Destino"].unique()

    departamento_sel = st.selectbox("Selecciona un departamento", departamentos)
    temporada_sel = st.selectbox("Selecciona una temporada", temporadas)

    #Filtrar datos
    data_filtrado = data_grouped[
        (data_grouped["Departamento"] == departamento_sel) &
        (data_grouped["Temporada"] == temporada_sel)
    ]

    #Crear dataframe con todos los destinos, incluso los que no aparecen
    destinos_df = pd.DataFrame({"Destino": destinos})
    data_filtrado = destinos_df.merge(data_filtrado, on="Destino", how="left")

    #Rellenar NaN con valores por defecto
    data_filtrado["Departamento"] = data_filtrado["Departamento"].fillna(departamento_sel)
    data_filtrado["Temporada"] = data_filtrado["Temporada"].fillna(temporada_sel)
    data_filtrado["Visitantes"] = data_filtrado["Visitantes"].fillna(0)

    #Graficar visitantes por destino
    fig = px.bar(
    data_filtrado,
    x="Destino",
    y="Visitantes",
    title=f"Visitantes en {departamento_sel} - {temporada_sel}",
    color="Visitantes",
    color_continuous_scale="blues",
    text="Visitantes"
    )

    fig.update_traces(
        texttemplate='%{text:.0f}',
        textposition='outside',
        marker_line_color='black',
        marker_line_width=1
    )

    fig.update_layout(
        xaxis_title="Destinos",
        yaxis_title="Número de Visitantes",
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("Muestra el número de visitantes por destino en el departamento y temporada seleccionados")

    #Mostrar tabla filtrada
    st.dataframe(data_filtrado)

    #BOXPLOT
    st.title("Boxplot de número de visitantes por Destino")

    # Selector de temporada para el boxplot
    temporada_boxplot = st.selectbox(
        "Selecciona la temporada para el boxplot:",
        options=data['Temporada'].unique(),
        key="boxplot_temporada"
    )

    # Filtrar datos por la temporada seleccionada
    data_boxplot = data[data['Temporada'] == temporada_boxplot].groupby(['Departamento', 'Destino'])['Visitantes'].mean().reset_index()

    # Crear boxplot interactivo con Plotly
    fig2 = px.box(
        data_boxplot,
        x="Destino",
        y="Visitantes",
        color="Destino",
        title=f"Distribución de Visitantes por Destino - Temporada {temporada_boxplot}",
        points="all", 
        hover_data=["Departamento"]
    )

    fig2.update_layout(
        xaxis_title="Destinos",
        yaxis_title="Número de Visitantes",
        xaxis_tickangle=-45,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=600,
        showlegend=False
    )

    fig2.update_traces(
        marker=dict(size=6, opacity=0.7),
        line=dict(width=2)
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.caption(f"Muestra la distribución de visitantes entre diferentes destinos en temporada {temporada_boxplot}, cada punto representa un departamento específico")