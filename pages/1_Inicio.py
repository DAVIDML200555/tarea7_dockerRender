import streamlit as st
from streamlit_option_menu import option_menu

# Ocultar sidebar nav nativo de Streamlit
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        text-align: center;
        margin: 2rem 0;
    }
    
    .stat-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        min-width: 120px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        "Menú Principal", 
        ["Inicio", "Dashboard", "Mapa"],  
        icons=["house", "bar-chart", "geo-alt"],  
        menu_icon="compass", 
        default_index=0,
        styles={
            "container": {"padding": "10px"},
            "icon": {"color": "#FF4B4B", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px"},
            "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
        }
    )

# Navegación
if selected == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")
elif selected == "Mapa":
    st.switch_page("pages/3_Mapa.py")

# Contenido de la página de Inicio
st.set_page_config(
    page_title="Turismo Colombia - Inicio", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Header principal
st.markdown('<h1 class="main-header">🏖️ Análisis de Turismo Nacional en Colombia</h1>', unsafe_allow_html=True)

# Introducción
st.markdown("""
### 🌟 Bienvenido a la Plataforma de Análisis Turístico

Esta aplicación permite **explorar y analizar datos de turismo nacional** en Colombia de manera 
interactiva a través de visualizaciones avanzadas, gráficos dinámicos y mapas interactivos 
para identificar patrones y tendencias en el sector turístico.
""")

# Estadísticas rápidas
st.markdown("### 📊 Resumen de Datos")
cols = st.columns(4)

with cols[0]:
    st.metric("Total Registros", "200", "Base completa")
with cols[1]:
    st.metric("Departamentos", "10+", "Diversidad regional")
with cols[2]:
    st.metric("Tipos de Destino", "4", "Montaña, Playa, Ciudad, Selva")
with cols[3]:
    st.metric("Temporadas", "3", "Alta, Media, Baja")

# Características principales
st.markdown("### 🎯 Funcionalidades Principales")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
    <div class="feature-card">
        <h4>📈 Dashboard Analítico</h4>
        <p>Visualiza estadísticas detalladas, gráficos comparativos y análisis por temporadas y destinos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🗺️ Mapa Interactivo</h4>
        <p>Explora la distribución geográfica de los destinos turísticos con filtros dinámicos.</p>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
    <div class="feature-card">
        <h4>📊 Gráficos Comparativos</h4>
        <p>Analiza patrones de visitantes mediante boxplots, barras y gráficos de distribución.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <h4>🔍 Filtros Avanzados</h4>
        <p>Personaliza tu análisis filtrando por departamento, destino y temporada turística.</p>
    </div>
    """, unsafe_allow_html=True)

# Objetivos específicos
st.markdown("### 🎯 Objetivos del Análisis")

st.markdown("""
- **Visualizar** el número de visitantes por destino y temporada
- **Analizar** la distribución por departamento mediante visualizaciones estadísticas  
- **Identificar** patrones estacionales en el turismo nacional
- **Explorar** correlaciones geográficas y preferencias de destino
- **Comparar** el comportamiento turístico entre diferentes regiones
""")

# Llamada a la acción
st.markdown("---")
st.markdown("""
### 🚀 ¿Listo para Explorar?

**Utiliza el menú lateral** para navegar entre las diferentes secciones y comenzar tu análisis del turismo colombiano.

**Dashboard**: Para análisis estadísticos detallados  
**Mapa**: Para exploración geográfica interactiva
""")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Desarrollado con Streamlit • Datos: Turismo Nacional Colombia"
    "</div>", 
    unsafe_allow_html=True
)