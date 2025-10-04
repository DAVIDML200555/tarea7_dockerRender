import streamlit as st
from streamlit_option_menu import option_menu
st.switch_page("pages/1_Inicio.py")


st.set_page_config(page_title="App con Mapas", layout="wide", initial_sidebar_state="collapsed")

with st.sidebar:
    selected = option_menu("Menú", 
        ["Inicio", "Dashboard", "Mapa"],  
        icons=["house", "bar-chart", "geo-alt"],  
        menu_icon="cast", 
        default_index=0
    )

if selected == "Inicio":
    st.switch_page("pages/1_Inicio.py")
elif selected == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")
elif selected == "Mapa":
    st.switch_page("pages/3_Mapa.py")