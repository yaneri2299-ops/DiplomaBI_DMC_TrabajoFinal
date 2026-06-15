
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="App Analizadora de Datasets", layout="wide")

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

def detect_dates(df):
    date_cols = []
    for c in df.columns:
        try:
            conv = pd.to_datetime(df[c], errors="coerce")
            if conv.notna().sum() > len(df)*0.5:
                df[c] = conv
                date_cols.append(c)
        except:
            pass
    return df, date_cols

st.title("📊 App Analizadora de Datasets con Streamlit")

menu = st.sidebar.radio(
    "Menú",
    ["Home","Carga y Perfil","Procesamiento","Análisis Visual"]
)

if "df" not in st.session_state:
    st.session_state.df = None

if menu=="Home":
    st.header("Proyecto Final Integrador")
    st.write("Autor: Yaneri Martinez")
    st.write("Tecnologías: Python, Pandas, Streamlit, Plotly, Matplotlib, Seaborn, GitHub")
    st.info("Resultados exploratorios. No reemplazan validación profesional.")
    st.markdown("""
    **Datasets soportados**
    - AI Impact on Jobs
    - Superstore
    - E-commerce Risk
    - Teen Mental Health
    """)

elif menu=="Carga y Perfil":
    archivo = st.file_uploader("Cargar CSV", type=["csv"])
    if archivo:
        df = load_data(archivo)
        st.session_state.df = df

    if st.session_state.df is not None:
        df = st.session_state.df
        st.subheader("Vista previa")
        st.dataframe(df.head())

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Filas", df.shape[0])
        c2.metric("Columnas", df.shape[1])
        c3.metric("Nulos", int(df.isna().sum().sum()))
        c4.metric("Duplicados", int(df.duplicated().sum()))

        st.write(df.dtypes)

elif menu=="Procesamiento":
    if st.session_state.df is None:
        st.warning("Cargue un dataset primero")
    else:
        df = st.session_state.df.copy()
        df.columns = [c.strip().replace(" ","_") for c in df.columns]

        df, date_cols = detect_dates(df)

        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        st.subheader("Clasificación de variables")
        st.write("Numéricas:", num_cols)
        st.write("Categóricas:", cat_cols)
        st.write("Fechas:", date_cols)

        st.subheader("Valores faltantes")
        nulls = pd.DataFrame({
            "columna":df.columns,
            "nulos":df.isna().sum(),
            "porcentaje":(df.isna().sum()/len(df))*100
        })
        st.dataframe(nulls)

        st.metric("Duplicados", int(df.duplicated().sum()))

elif menu=="Análisis Visual":
    if st.session_state.df is None:
        st.warning("Cargue un dataset primero")
    else:
        df = st.session_state.df.copy()
        df, date_cols = detect_dates(df)

        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        tabs = st.tabs(["Resumen","Univariado","Bivariado","Multivariado","Temporal","Insights"])

        with tabs[0]:
            st.dataframe(df.describe(include="all"))

        with tabs[1]:
            if num_cols:
                col = st.selectbox("Variable numérica", num_cols)
                fig = px.histogram(df, x=col)
                st.plotly_chart(fig, use_container_width=True)

                fig2, ax = plt.subplots()
                sns.boxplot(x=df[col], ax=ax)
                st.pyplot(fig2)

        with tabs[2]:
            if len(num_cols)>=2:
                x = st.selectbox("X", num_cols, key="x")
                y = st.selectbox("Y", num_cols, key="y")
                fig = px.scatter(df,x=x,y=y)
                st.plotly_chart(fig,use_container_width=True)

        with tabs[3]:
            if len(num_cols)>=2:
                corr = df[num_cols].corr()
                fig, ax = plt.subplots(figsize=(8,5))
                sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)

        with tabs[4]:
            if date_cols and num_cols:
                d = st.selectbox("Fecha", date_cols)
                n = st.selectbox("Métrica", num_cols)
                temp = df.groupby(d)[n].mean().reset_index()
                fig = px.line(temp,x=d,y=n)
                st.plotly_chart(fig,use_container_width=True)

        with tabs[5]:
            st.success("Generar conclusiones según los gráficos observados.")
