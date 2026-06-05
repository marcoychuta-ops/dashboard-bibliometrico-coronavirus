
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Dashboard Bibliométrico",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
}

[data-testid="metric-container"]{
    background-color:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    border:1px solid #EAEAEA;
}

h1{
    color:#0A3D62;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CARGA DE DATOS
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("coronavirus_detection.csv")

df = load_data()

# --------------------------------------------------
# LIMPIEZA
# --------------------------------------------------

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)

# --------------------------------------------------
# FILTROS
# --------------------------------------------------

st.sidebar.title("🔎 Filtros")

min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

year_range = st.sidebar.slider(
    "Year",
    min_year,
    max_year,
    (min_year, max_year)
)

source_filter = st.sidebar.multiselect(
    "Source title",
    sorted(df["Source title"].dropna().unique())
)

document_filter = st.sidebar.multiselect(
    "Document Type",
    sorted(df["Document Type"].dropna().unique())
)

filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

if source_filter:
    filtered_df = filtered_df[
        filtered_df["Source title"].isin(source_filter)
    ]

if document_filter:
    filtered_df = filtered_df[
        filtered_df["Document Type"].isin(document_filter)
    ]

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------

st.title("📚 Dashboard Bibliométrico")
st.markdown("### Coronavirus Detection Research")

# --------------------------------------------------
# KPIs
# --------------------------------------------------

total_publicaciones = len(filtered_df)
total_revistas = filtered_df["Source title"].nunique()
total_citas = filtered_df["Cited by"].sum()
promedio_citas = filtered_df["Cited by"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("📄 Publicaciones", total_publicaciones)
c2.metric("📚 Revistas", total_revistas)
c3.metric("⭐ Promedio Citaciones", round(promedio_citas, 2))
c4.metric("📈 Total Citaciones", int(total_citas))

st.divider()

# --------------------------------------------------
# PUBLICACIONES POR AÑO
# --------------------------------------------------

pub_year = (
    filtered_df.groupby("Year")
    .size()
    .reset_index(name="Publicaciones")
)

fig_year = px.line(
    pub_year,
    x="Year",
    y="Publicaciones",
    markers=True,
    title="📈 Publicaciones por Año"
)

st.plotly_chart(fig_year, use_container_width=True)

# --------------------------------------------------
# TOP REVISTAS
# --------------------------------------------------

col1, col2 = st.columns(2)

top_sources = (
    filtered_df["Source title"]
    .value_counts()
    .head(5)
    .reset_index()
)

top_sources.columns = ["Revista", "Cantidad"]

fig_sources = px.bar(
    top_sources,
    x="Revista",
    y="Cantidad",
    color="Cantidad",
    color_continuous_scale="Viridis",
    title="🏛 Top Revistas"
)

fig_sources.update_traces(width=0.6)

fig_sources.update_layout(
    height=600,
    xaxis_title="Revista",
    yaxis_title="Cantidad",
    xaxis_tickangle=-45
)

col1.plotly_chart(
    fig_sources,
    use_container_width=True
)

# --------------------------------------------------
# TOP AUTORES
# --------------------------------------------------

authors = (
    filtered_df["Author full names"]
    .dropna()
    .str.split(";")
    .explode()
    .str.strip()
)

top_authors = (
    authors.value_counts()
    .head(15)
    .reset_index()
)

top_authors.columns = ["Autor", "Publicaciones"]

fig_authors = px.bar(
    top_authors,
    x="Publicaciones",
    y="Autor",
    orientation="h",
    color="Publicaciones",
    color_continuous_scale="Plasma",
    title="👨‍🔬 Top 15 Autores"
)

col2.plotly_chart(
    fig_authors,
    use_container_width=True
)

# --------------------------------------------------
# TOP ARTÍCULOS MÁS CITADOS
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

fig_cited.update_yaxes(autorange="reversed")

st.plotly_chart(
    fig_cited,
    use_container_width=True
)

# --------------------------------------------------
# TABLA
# --------------------------------------------------

st.subheader("📑 Registro Bibliográfico")

cols = [
    "Title",
    "Author full names",
    "Year",
    "Source title",
    "Cited by",
    "DOI"
]

st.dataframe(
    filtered_df[cols],
    use_container_width=True,
    height=500
)

# --------------------------------------------------
# DESCARGA
# --------------------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Descargar Datos Filtrados",
    csv,
    "bibliometria_filtrada.csv",
    "text/csv"
)
