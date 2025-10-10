import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de página DEBE ir al principio
st.set_page_config(
    page_title="Dashboard Turístico - Colombia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilos CSS mejorados
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 0.5rem 0;
    }
    
    .section-header {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("📊 Filtros")
    st.markdown("---")
    
    selected = option_menu(
        "Menú Principal", 
        ["Inicio", "Dashboard", "Mapa"],  
        icons=["house", "bar-chart", "geo-alt"],  
        menu_icon="compass", 
        default_index=1,
        styles={
            "container": {"padding": "10px"},
            "icon": {"color": "#FF4B4B", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px"},
            "nav-link-selected": {"background-color": "#4CAF50", "color": "white"},
        }
    )

# Navegación
if selected == "Inicio":
    st.switch_page("pages/1_Inicio.py")
elif selected == "Mapa":
    st.switch_page("pages/3_Mapa.py")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("data/turismo_nacional.csv")

data = load_data()
data_grouped = data.groupby(['Departamento', 'Destino', 'Temporada'])['Visitantes'].mean().reset_index()

# Header principal
st.title("📊 Dashboard Analítico - Turismo Nacional")
st.markdown("Análisis completo de visitantes por departamento, destino y temporada")

# ========== SECCIÓN 1: MÉTRICAS PRINCIPALES ==========
st.markdown('<h3 class="section-header">📈 Métricas Generales</h3>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Departamentos", 
        data['Departamento'].nunique(),
        "Regiones analizadas"
    )

with col2:
    st.metric(
        "Tipos de Destino", 
        data['Destino'].nunique(),
        "Categorías turísticas"
    )

with col3:
    total_visitantes = data['Visitantes'].sum()
    st.metric(
        "Visitantes Totales", 
        f"{total_visitantes:,}",
        "Acumulado general"
    )

with col4:
    st.metric(
        "Temporadas", 
        data['Temporada'].nunique(),
        "Alta, Media, Baja"
    )

# Métricas estadísticas
col5, col6, col7, col8 = st.columns(4)

with col5:
    media_visitantes = data['Visitantes'].mean()
    st.metric("Media Visitantes", f"{media_visitantes:.0f}")

with col6:
    max_visitantes = data['Visitantes'].max()
    st.metric("Máximo Visitantes", f"{max_visitantes:,}")

with col7:
    min_visitantes = data['Visitantes'].min()
    st.metric("Mínimo Visitantes", f"{min_visitantes:,}")

with col8:
    std_visitantes = data['Visitantes'].std()
    st.metric("Desviación Estándar", f"{std_visitantes:.0f}")

# ========== SECCIÓN 2: ANÁLISIS POR DEPARTAMENTO ==========
st.markdown('<h3 class="section-header"> Análisis por Departamento</h3>', unsafe_allow_html=True)

col_sel1, col_sel2 = st.columns(2)

with col_sel1:
    departamentos = data_grouped["Departamento"].unique()
    departamento_sel = st.selectbox(
        "Selecciona un departamento:", 
        departamentos,
        help="Selecciona un departamento para analizar sus destinos turísticos"
    )

with col_sel2:
    temporadas = data_grouped["Temporada"].unique()
    temporada_sel = st.selectbox(
        "Selecciona una temporada:", 
        temporadas,
        help="Filtra por temporada turística"
    )

# Filtrar datos
data_filtrado = data_grouped[
    (data_grouped["Departamento"] == departamento_sel) &
    (data_grouped["Temporada"] == temporada_sel)
]

# Crear dataframe con todos los destinos
destinos = data_grouped["Destino"].unique()
destinos_df = pd.DataFrame({"Destino": destinos})
data_filtrado = destinos_df.merge(data_filtrado, on="Destino", how="left")
data_filtrado["Departamento"] = data_filtrado["Departamento"].fillna(departamento_sel)
data_filtrado["Temporada"] = data_filtrado["Temporada"].fillna(temporada_sel)
data_filtrado["Visitantes"] = data_filtrado["Visitantes"].fillna(0)

# Gráfico de barras mejorado
fig_barras = px.bar(
    data_filtrado,
    x="Destino",
    y="Visitantes",
    title=f"Visitantes por Destino en {departamento_sel} - Temporada {temporada_sel}",
    color="Visitantes",
    color_continuous_scale="viridis",
    text="Visitantes",
    hover_data={"Destino": True, "Visitantes": ":.0f"}
)

fig_barras.update_traces(
    texttemplate='%{text:.0f}',
    textposition='outside',
    marker_line_color='black',
    marker_line_width=1,
    hovertemplate="<b>%{x}</b><br>Visitantes: %{y:.0f}<extra></extra>"
)

fig_barras.update_layout(
    xaxis_title="Destinos Turísticos",
    yaxis_title="Número de Visitantes",
    xaxis_tickangle=-45,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12),
    height=500,
    showlegend=False
)

st.plotly_chart(fig_barras, use_container_width=True)
st.caption(f"Distribución de visitantes por tipo de destino en {departamento_sel} durante temporada {temporada_sel}")

# ========== SECCIÓN 3: ANÁLISIS COMPARATIVO ==========
st.markdown('<h3 class="section-header">📋 Análisis Comparativo</h3>', unsafe_allow_html=True)

col_tab1, col_tab2 = st.columns([2, 1])

with col_tab1:
    # Mostrar tabla filtrada con mejor formato
    st.subheader("Datos Detallados")
    data_filtrado_display = data_filtrado.copy()
    data_filtrado_display['Visitantes'] = data_filtrado_display['Visitantes'].astype(int)
    st.dataframe(
        data_filtrado_display,
        use_container_width=True,
        hide_index=True
    )

with col_tab2:
    st.subheader("📈 Resumen Estadístico")
    
    # Estadísticas rápidas del departamento seleccionado
    visitantes_totales = data_filtrado['Visitantes'].sum()
    destinos_con_visitantes = (data_filtrado['Visitantes'] > 0).sum()
    
    st.metric("Visitantes Totales", f"{visitantes_totales:,.0f}")
    st.metric("Destinos Activos", destinos_con_visitantes)
    st.metric("Destino Más Visitado", 
              data_filtrado.loc[data_filtrado['Visitantes'].idxmax(), 'Destino'] 
              if visitantes_totales > 0 else "Sin datos")

# ========== SECCIÓN 4: ANÁLISIS DE DISTRIBUCIÓN ==========
st.markdown('<h3 class="section-header">📦 Análisis de Distribución</h3>', unsafe_allow_html=True)

col_box1, col_box2 = st.columns([1, 4])

with col_box1:
    temporada_boxplot = st.selectbox(
        "Selecciona temporada para análisis:",
        options=data['Temporada'].unique(),
        key="boxplot_temporada",
        help="Analiza la distribución de visitantes por destino en esta temporada"
    )

# Preparar datos para boxplot
data_boxplot = data[data['Temporada'] == temporada_boxplot]

# Crear boxplot interactivo mejorado
fig_boxplot = px.box(
    data_boxplot,
    x="Destino",
    y="Visitantes",
    color="Destino",
    title=f"Distribución de Visitantes por Destino - Temporada {temporada_boxplot}",
    points="all",
    hover_data=["Departamento"],
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig_boxplot.update_layout(
    xaxis_title="Destinos Turísticos",
    yaxis_title="Número de Visitantes",
    xaxis_tickangle=-45,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12),
    height=600,
    showlegend=False
)

fig_boxplot.update_traces(
    marker=dict(size=6, opacity=0.7, line=dict(width=1, color='DarkSlateGrey')),
    line=dict(width=2),
    hovertemplate="<b>%{x}</b><br>Departamento: %{customdata[0]}<br>Visitantes: %{y:.0f}<extra></extra>"
)

st.plotly_chart(fig_boxplot, use_container_width=True)
st.caption(f"Distribución de visitantes entre diferentes destinos en temporada {temporada_boxplot}. Cada punto representa un departamento específico")

# ========== SECCIÓN 5: ANÁLISIS ADICIONAL ==========
st.markdown('<h3 class="section-header">🔍 Análisis Adicional</h3>', unsafe_allow_html=True)

# Top departamentos por visitantes
col_anal1, col_anal2 = st.columns(2)

with col_anal1:
    st.subheader("🏆 Top 5 Departamentos")
    top_deptos = data.groupby('Departamento')['Visitantes'].sum().nlargest(5).reset_index()
    fig_top = px.bar(
        top_deptos,
        x='Visitantes',
        y='Departamento',
        orientation='h',
        title="Departamentos con Más Visitantes",
        color='Visitantes',
        color_continuous_scale='teal'
    )
    fig_top.update_layout(height=300)
    st.plotly_chart(fig_top, use_container_width=True)

with col_anal2:
    st.subheader("🌤️ Visitantes por Temporada")
    temp_stats = data.groupby('Temporada')['Visitantes'].sum().reset_index()
    fig_temp = px.pie(
        temp_stats,
        values='Visitantes',
        names='Temporada',
        title="Distribución por Temporada",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_temp.update_layout(height=300)
    st.plotly_chart(fig_temp, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Dashboard desarrollado con Streamlit • Datos: Turismo Nacional Colombia"
    "</div>", 
    unsafe_allow_html=True
)