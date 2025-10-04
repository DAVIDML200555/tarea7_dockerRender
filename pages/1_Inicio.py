import streamlit as st
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
        default_index=0
    )

if selected == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")
elif selected == "Mapa":
    st.switch_page("pages/3_Mapa.py")
else:
    st.set_page_config(page_title="Mapa Visitantes", layout="wide", initial_sidebar_state="collapsed")
    st.title("Bienvenido a la App Interactiva del Turismo en Colombia")

    st.markdown("""
    Esta aplicación permite **explorar y analizar datos de turismo nacional** en Colombia de manera sencilla e interactiva a 
        través de gráficos, tablas y mapas dinámicos con el fin de identificar patrones y comparaciones entre destinos, temporadas y departamentos.

    ### Objetivos principales
    - Visualizar el número de **visitantes por destino y temporada**.
    - Analizar la **distribución por departamento y destino** mediante boxplots.
    - Explorar un **mapa interactivo** con localización geográfica y filtros dinámicos.

    Usa los menús laterales y los filtros para navegar entre secciones y personalizar tu análisis.
    """)