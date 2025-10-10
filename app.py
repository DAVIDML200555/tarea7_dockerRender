import streamlit as st
from streamlit_option_menu import option_menu

# Configuración DEBE ir al principio
st.set_page_config(
    page_title="Turismo Nacional App",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Menú en sidebar con mejor diseño
with st.sidebar:
    st.title("🏖️ Turismo Nacional")
    st.markdown("---")
    
    selected = option_menu(
        menu_title="Navegación",
        options=["Inicio", "Dashboard", "Mapa"],
        icons=["house", "bar-chart", "geo-alt"],
        menu_icon="compass",
        default_index=0,
        styles={
            "container": {"padding": "5px"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "2px"},
            "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
        }
    )
    
    # Información adicional en sidebar
    st.markdown("---")
    st.markdown("### 📊 Datos")
    st.info("Base de datos: turismo_nacional.csv")
    st.markdown("**200 registros** de destinos turísticos")

# Navegación a páginas
if selected == "Inicio":
    st.switch_page("pages/1_Inicio.py")
elif selected == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")
elif selected == "Mapa":
    st.switch_page("pages/3_Mapa.py")