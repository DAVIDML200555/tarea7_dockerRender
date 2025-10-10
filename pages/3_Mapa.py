import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from branca.colormap import LinearColormap
from streamlit_option_menu import option_menu
import plotly.express as px

# Configuración de página DEBE ir al principio
st.set_page_config(
    page_title="Mapa Interactivo - Turismo Colombia", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilos CSS mejorados
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    .map-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
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
    st.title("🗺️ Controles del Mapa")
    st.markdown("---")
    
    selected = option_menu(
        "Menú Principal", 
        ["Inicio", "Dashboard", "Mapa"],  
        icons=["house", "bar-chart", "geo-alt"],  
        menu_icon="compass", 
        default_index=2,
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
elif selected == "Dashboard":
    st.switch_page("pages/2_Dashboard.py")

# Header principal
st.markdown("""
<div class="map-header">
    <h1 style="margin:0; color:white;">🗺️ Mapa Interactivo de Turismo Nacional</h1>
    <p style="margin:0; opacity:0.9;">Explora la distribución geográfica de visitantes en Colombia</p>
</div>
""", unsafe_allow_html=True)

# Cargar datos con cache
@st.cache_data
def load_data():
    return pd.read_csv("data/turismo_nacional.csv")

data = load_data()

# Agrupar y calcular promedio de visitantes
data_grouped = data.groupby(['Departamento', 'Destino', 'Temporada', 'Latitud', 'Longitud'])['Visitantes'].mean().reset_index()

# ========== SECCIÓN 1: FILTROS Y CONTROLES ==========
st.markdown('<h3 class="section-header">🎛️ Controles del Mapa</h3>', unsafe_allow_html=True)

col_filt1, col_filt2, col_filt3, col_filt4 = st.columns(4)

with col_filt1:
    destinos = data_grouped["Destino"].unique()
    destino_sel = st.selectbox(
        "Tipo de Destino", 
        destinos,
        help="Selecciona el tipo de destino turístico a visualizar"
    )

with col_filt2:
    temporadas = data_grouped["Temporada"].unique()
    temporada_sel = st.selectbox(
        "Temporada Turística", 
        temporadas,
        help="Filtra por temporada alta, media o baja"
    )

with col_filt3:
    # Control de tamaño de marcadores
    escala_marcadores = st.slider(
        "Tamaño de marcadores",
        min_value=100,
        max_value=2000,
        value=500,
        step=100,
        help="Ajusta el tamaño de los círculos en el mapa"
    )

with col_filt4:
    # Opacidad de los marcadores
    opacidad = st.slider(
        "Opacidad de marcadores",
        min_value=0.1,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controla la transparencia de los círculos"
    )

# ========== SECCIÓN 2: MÉTRICAS RÁPIDAS ==========
st.markdown('<h3 class="section-header">📊 Resumen de Datos Filtrados</h3>', unsafe_allow_html=True)

# Filtrar datos según selección
data_filtrado = data_grouped[
    (data_grouped["Destino"] == destino_sel) &
    (data_grouped["Temporada"] == temporada_sel)
]

# Métricas
col_met1, col_met2, col_met3, col_met4 = st.columns(4)

with col_met1:
    st.metric(
        "Departamentos", 
        data_filtrado['Departamento'].nunique(),
        "Con datos"
    )

with col_met2:
    total_visitantes = data_filtrado['Visitantes'].sum()
    st.metric(
        "Visitantes Totales", 
        f"{total_visitantes:,.0f}",
        "Promedio acumulado"
    )

with col_met3:
    max_visitantes = data_filtrado['Visitantes'].max()
    st.metric(
        "Máximo Visitantes", 
        f"{max_visitantes:,.0f}",
        "En un departamento"
    )

with col_met4:
    depto_max = data_filtrado.loc[data_filtrado['Visitantes'].idxmax(), 'Departamento'] if not data_filtrado.empty else "N/A"
    st.metric(
        "Departamento Líder", 
        depto_max,
        "Más visitantes"
    )

# ========== SECCIÓN 3: MAPA INTERACTIVO ==========
st.markdown('<h3 class="section-header">🗺️ Visualización en Mapa</h3>', unsafe_allow_html=True)

if data_filtrado.empty:
    st.warning("⚠️ No hay datos disponibles para la combinación seleccionada. Por favor, ajusta los filtros.")
else:
    # Crear mapa base
    m = folium.Map(
        location=[4.6097, -74.0818], 
        zoom_start=5,
        tiles='OpenStreetMap',  # Puedes cambiar a 'CartoDB positron' para un estilo más claro
        control_scale=True
    )

    # Crear escala de colores mejorada
    min_val, max_val = data_filtrado['Visitantes'].min(), data_filtrado['Visitantes'].max()
    
    # Escala de colores más atractiva
    colormap = LinearColormap(
        colors=["#2E8B57", "#FFD700", "#FF4500"],  # Verde -> Amarillo -> Rojo
        vmin=min_val, 
        vmax=max_val,
        caption=f'Rango de Visitantes ({destino_sel} - {temporada_sel})'
    )

    # Añadir círculos al mapa con mejoras
    for _, row in data_filtrado.iterrows():
        # Calcular radio proporcional (evitar círculos demasiado pequeños/grandes)
        radius = max(5, min(50, row['Visitantes'] / escala_marcadores))
        
        folium.CircleMarker(
            location=[row['Latitud'], row['Longitud']],
            radius=radius,
            color=colormap(row['Visitantes']),
            fill=True,
            fill_color=colormap(row['Visitantes']),
            fill_opacity=opacidad,
            weight=2,
            popup=folium.Popup(
                f"""
                <div style="font-family: Arial; min-width: 200px;">
                    <h4 style="margin:0; color: #1f77b4;">{row['Departamento']}</h4>
                    <hr style="margin: 5px 0;">
                    <p style="margin:2px 0;"><strong>Destino:</strong> {row['Destino']}</p>
                    <p style="margin:2px 0;"><strong>Temporada:</strong> {row['Temporada']}</p>
                    <p style="margin:2px 0;"><strong>Visitantes:</strong> {row['Visitantes']:,.0f}</p>
                    <p style="margin:2px 0;"><strong>Coordenadas:</strong> {row['Latitud']:.4f}, {row['Longitud']:.4f}</p>
                </div>
                """,
                max_width=300
            ),
            tooltip=f"{row['Departamento']}: {row['Visitantes']:,.0f} visitantes"
        ).add_to(m)

    # Añadir leyenda al mapa
    colormap.add_to(m)

    # Añadir control de capas
    folium.LayerControl().add_to(m)

    # Mostrar mapa
    col_map1, col_map2 = st.columns([3, 1])

    with col_map1:
        st_folium(m, width=900, height=600, returned_objects=[])
        
        st.caption("""
        **Interpretación del mapa:**
        - Los círculos representan la cantidad de visitantes (tamaño proporcional)
        - El color indica la intensidad (verde = menor, rojo = mayor)
        - Haz clic en cualquier marcador para ver detalles específicos
        """)

    with col_map2:
        st.markdown("### 📋 Datos del Mapa")
        
        # Mostrar tabla resumen
        if not data_filtrado.empty:
            tabla_resumen = data_filtrado[['Departamento', 'Visitantes']].sort_values('Visitantes', ascending=False)
            tabla_resumen['Visitantes'] = tabla_resumen['Visitantes'].apply(lambda x: f"{x:,.0f}")
            st.dataframe(
                tabla_resumen,
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Botón para descargar datos filtrados
            csv = data_filtrado.to_csv(index=False)
            st.download_button(
                label="📥 Descargar datos filtrados",
                data=csv,
                file_name=f"turismo_{destino_sel}_{temporada_sel}.csv",
                mime="text/csv"
            )

# ========== SECCIÓN 4: ANÁLISIS ADICIONAL ==========
st.markdown('<h3 class="section-header">📈 Análisis Complementario</h3>', unsafe_allow_html=True)

if not data_filtrado.empty:
    col_anal1, col_anal2 = st.columns(2)
    
    with col_anal1:
        # Gráfico de barras horizontal
        fig_barras = px.bar(
            data_filtrado.sort_values('Visitantes', ascending=True),
            y='Departamento',
            x='Visitantes',
            title=f"Visitantes por Departamento - {destino_sel} ({temporada_sel})",
            orientation='h',
            color='Visitantes',
            color_continuous_scale='viridis'
        )
        fig_barras.update_layout(height=400)
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col_anal2:
        # Mapa de calor de densidad
        fig_densidad = px.density_mapbox(
            data_filtrado,
            lat='Latitud',
            lon='Longitud',
            z='Visitantes',
            radius=30,
            center=dict(lat=4.6097, lon=-74.0818),
            zoom=4,
            mapbox_style="open-street-map",
            title=f"Densidad de Visitantes - {destino_sel} ({temporada_sel})",
            hover_data=['Departamento']
        )
        fig_densidad.update_layout(height=400)
        st.plotly_chart(fig_densidad, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Mapa interactivo desarrollado con Streamlit y Folium • Datos: Turismo Nacional Colombia"
    "</div>", 
    unsafe_allow_html=True
)