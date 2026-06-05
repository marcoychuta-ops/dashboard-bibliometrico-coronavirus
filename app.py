import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: white;
}

.main {
    background-color: white;
}

section[data-testid="stSidebar"] {
    background-color: #F8F9FA;
}

[data-testid="metric-container"]{
    background-color:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    border:1px solid #EAEAEA;
}

h1,h2,h3{
    color:#0A3D62;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CONFIGURACIÓN GLOBAL DE PLOTLY
# --------------------------------------------------

PLOTLY_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5,
    font=dict(size=14)
)

# --------------------------------------------------
# PUBLICACIONES POR AÑO
# --------------------------------------------------

fig_year = px.line(
    pub_year,
    x="Year",
    y="Publicaciones",
    markers=True,
    title="📈 Publicaciones por Año",
    color_discrete_sequence=["#1F77B4"]
)

fig_year.update_layout(**PLOTLY_LAYOUT)

st.plotly_chart(
    fig_year,
    use_container_width=True
)

# --------------------------------------------------
# TOP SOURCE TITLE
# --------------------------------------------------

fig_sources = px.bar(
    top_sources,
    x="Cantidad",
    y="Source",
    orientation="h",
    color="Cantidad",
    color_continuous_scale="Viridis",
    title="🏛 Top 10 Source Title"
)

fig_sources.update_layout(**PLOTLY_LAYOUT)

col1.plotly_chart(
    fig_sources,
    use_container_width=True
)

# --------------------------------------------------
# TOP AUTORES
# --------------------------------------------------

fig_authors = px.bar(
    top_authors,
    x="Publicaciones",
    y="Autor",
    orientation="h",
    color="Publicaciones",
    color_continuous_scale="Plasma",
    title="👨‍🔬 Top 15 Autores"
)

fig_authors.update_layout(**PLOTLY_LAYOUT)

col2.plotly_chart(
    fig_authors,
    use_container_width=True
)

# --------------------------------------------------
# DOCUMENT TYPE
# --------------------------------------------------

fig_doc = px.pie(
    doc_type,
    names="Tipo",
    values="Cantidad",
    hole=0.55,
    title="📄 Document Type",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig_doc.update_layout(**PLOTLY_LAYOUT)

col3.plotly_chart(
    fig_doc,
    use_container_width=True
)

# --------------------------------------------------
# PUBLICATION STAGE
# --------------------------------------------------

fig_stage = px.pie(
    stage_data,
    names="Stage",
    values="Cantidad",
    hole=0.55,
    title="🚀 Publication Stage",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_stage.update_layout(**PLOTLY_LAYOUT)

col4.plotly_chart(
    fig_stage,
    use_container_width=True
)

# --------------------------------------------------
# TOP 10 ARTÍCULOS MÁS CITADOS
# --------------------------------------------------

top_cited = (
    filtered_df
    .sort_values(by="Cited by", ascending=False)
    .head(10)
)

fig_cited = px.bar(
    top_cited,
    x="Cited by",
    y="Title",
    orientation="h",
    color="Cited by",
    color_continuous_scale="Turbo",
    title="🏆 Top 10 Artículos Más Citados"
)

fig_cited.update_yaxes(
    autorange="reversed"
)

fig_cited.update_layout(**PLOTLY_LAYOUT)

st.plotly_chart(
    fig_cited,
    use_container_width=True
)

# --------------------------------------------------
# TABLA MEJORADA
# --------------------------------------------------

st.dataframe(
    filtered_df[cols],
    use_container_width=True,
    height=600,
    hide_index=True
)
