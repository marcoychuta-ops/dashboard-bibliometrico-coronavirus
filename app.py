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

.main {
    background-color: #F5F7FA;
}

[data-testid="metric-container"]{
    background-color:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.10);
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
    df = pd.read_csv("coronavirus_detection.csv")
    return df

df = load_data()


# --------------------------------------------------

# LIMPIEZA

# --------------------------------------------------

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Cited by"] = pd.to_numeric(df["Cited by"], errors="coerce").fillna(0)

# --------------------------------------------------

# SIDEBAR

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

open_access_filter = st.sidebar.multiselect(
"Open Access",
sorted(df["Open Access"].dropna().unique())
)

stage_filter = st.sidebar.multiselect(
"Publication Stage",
sorted(df["Publication Stage"].dropna().unique())
)

# --------------------------------------------------

# FILTROS

# --------------------------------------------------

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

if open_access_filter:
    filtered_df = filtered_df[
        filtered_df["Open Access"].isin(open_access_filter)
    ]

if stage_filter:
    filtered_df = filtered_df[
        filtered_df["Publication Stage"].isin(stage_filter)
    ]

# --------------------------------------------------

# TITULO

# --------------------------------------------------

st.title("📚 Dashboard Bibliométrico")
st.markdown("### Coronavirus Detection Research")

# --------------------------------------------------

# KPIs

# --------------------------------------------------

total_publicaciones = len(filtered_df)

total_source = filtered_df["Source title"].nunique()

promedio_citas = filtered_df["Cited by"].mean()

total_citas = filtered_df["Cited by"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
"📄 Total Publicaciones",
f"{total_publicaciones:,}"
)

c2.metric(
"📚 Total Source Title",
f"{total_source:,}"
)

c3.metric(
"⭐ Promedio Cited By",
f"{promedio_citas:.2f}"
)

c4.metric(
"📈 Total Cited By",
f"{int(total_citas):,}"
)

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
title="Publicaciones por Año"
)

st.plotly_chart(fig_year, use_container_width=True)

# --------------------------------------------------

# TOP SOURCE TITLE

# --------------------------------------------------

col1, col2 = st.columns(2)

top_sources = (
filtered_df["Source title"]
.value_counts()
.head(10)
.reset_index()
)

top_sources.columns = ["Source", "Cantidad"]

fig_sources = px.bar(
top_sources,
x="Cantidad",
y="Source",
orientation="h",
title="Top 10 Source Title"
)

col1.plotly_chart(
fig_sources,
use_container_width=True
)

# --------------------------------------------------

# AUTORES

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
title="Top 15 Autores"
)

col2.plotly_chart(
fig_authors,
use_container_width=True
)

# --------------------------------------------------

# DOCUMENT TYPE

# --------------------------------------------------

col3, col4 = st.columns(2)

doc_type = (
filtered_df["Document Type"]
.value_counts()
.reset_index()
)

doc_type.columns = ["Tipo", "Cantidad"]

fig_doc = px.pie(
doc_type,
names="Tipo",
values="Cantidad",
hole=0.5,
title="Document Type"
)

col3.plotly_chart(
fig_doc,
use_container_width=True
)

# --------------------------------------------------

# PUBLICATION STAGE

# --------------------------------------------------

stage_data = (
filtered_df["Publication Stage"]
.value_counts()
.reset_index()
)

stage_data.columns = ["Stage", "Cantidad"]

fig_stage = px.pie(
stage_data,
names="Stage",
values="Cantidad",
hole=0.5,
title="Publication Stage"
)

col4.plotly_chart(
fig_stage,
use_container_width=True
)

# --------------------------------------------------

# TOP ARTÍCULOS MÁS CITADOS

# --------------------------------------------------

top_cited = (
filtered_df.sort_values(
by="Cited by",
ascending=False
)
.head(10)
)

fig_cited = px.bar(
top_cited,
x="Cited by",
y="Title",
orientation="h",
title="Top 10 Artículos Más Citados"
)

st.plotly_chart(
fig_cited,
use_container_width=True
)

# --------------------------------------------------

# REGISTRO BIBLIOGRÁFICO

# --------------------------------------------------

st.subheader("📑 Registro Bibliográfico")

cols = [
"Title",
"Author full names",
"Year",
"Source title",
"Volume",
"Cited by",
"Link"
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
