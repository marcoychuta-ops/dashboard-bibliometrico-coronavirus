import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# ESTILOS
# --------------------------------------------------

# ==================================================
# KPIs
# ==================================================

total_publicaciones = len(filtered_df)

total_autores = (
    filtered_df["Author full names"]
    .dropna()
    .str.split(";")
    .explode()
    .nunique()
)

total_revistas = filtered_df["Source title"].nunique()

total_citas = filtered_df["Cited by"].sum()

promedio_citas = filtered_df["Cited by"].mean()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("📄 Publicaciones", total_publicaciones)
c2.metric("👨‍🔬 Autores", total_autores)
c3.metric("📚 Revistas", total_revistas)
c4.metric("📈 Citaciones", int(total_citas))
c5.metric("⭐ Promedio", round(promedio_citas, 2))

st.divider()

# ==================================================
# PUBLICACIONES POR AÑO
# ==================================================

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
    title="📈 Producción Científica por Año"
)

fig_year.update_layout(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5
)

st.plotly_chart(
    fig_year,
    use_container_width=True
)

# ==================================================
# TOP REVISTAS Y AUTORES
# ==================================================

col1, col2 = st.columns(2)

# Top Revistas

top_sources = (
    filtered_df["Source title"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_sources.columns = ["Revista", "Publicaciones"]

fig_sources = px.bar(
    top_sources,
    x="Publicaciones",
    y="Revista",
    orientation="h",
    color="Publicaciones",
    color_continuous_scale="Viridis",
    title="🏛 Top 10 Revistas"
)

fig_sources.update_yaxes(autorange="reversed")

fig_sources.update_layout(
    template="plotly_white",
    title_x=0.5
)

col1.plotly_chart(
    fig_sources,
    use_container_width=True
)

# Top Autores

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

fig_authors.update_yaxes(autorange="reversed")

fig_authors.update_layout(
    template="plotly_white",
    title_x=0.5
)

col2.plotly_chart(
    fig_authors,
    use_container_width=True
)

# ==================================================
# DOCUMENT TYPE Y OPEN ACCESS
# ==================================================

col3, col4 = st.columns(2)

# Document Type

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
    title="📄 Tipo de Documento",
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig_doc.update_layout(
    template="plotly_white",
    title_x=0.5
)

col3.plotly_chart(
    fig_doc,
    use_container_width=True
)

# Open Access

oa = (
    filtered_df["Open Access"]
    .value_counts()
    .reset_index()
)

oa.columns = ["Acceso", "Cantidad"]

fig_oa = px.pie(
    oa,
    names="Acceso",
    values="Cantidad",
    hole=0.5,
    title="🔓 Open Access",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_oa.update_layout(
    template="plotly_white",
    title_x=0.5
)

col4.plotly_chart(
    fig_oa,
    use_container_width=True
)

# ==================================================
# TOP 10 ARTÍCULOS MÁS CITADOS
# ==================================================

top_cited = (
    filtered_df
    .sort_values(
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
    color="Cited by",
    color_continuous_scale="Turbo",
    title="🏆 Top 10 Artículos Más Citados"
)

fig_cited.update_yaxes(
    autorange="reversed"
)

fig_cited.update_layout(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_x=0.5
)

st.plotly_chart(
    fig_cited,
    use_container_width=True
)

# ==================================================
# TABLA BIBLIOGRÁFICA
# ==================================================

st.subheader("📑 Registro Bibliográfico")

cols = [
    "Title",
    "Author full names",
    "Year",
    "Source title",
    "Document Type",
    "Open Access",
    "Cited by",
    "DOI"
]

st.dataframe(
    filtered_df[cols],
    use_container_width=True,
    height=600,
    hide_index=True
)
