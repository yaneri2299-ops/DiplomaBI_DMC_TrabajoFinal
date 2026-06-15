
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="App Analizadora de Datasets", layout="wide")

def load_data(file):
    return pd.read_csv(file)


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


        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        st.subheader("Clasificación de variables")
        st.write("Categóricas:", cat_cols)

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

        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        tabs = st.tabs([
    "Resumen",
    "Distribución",
    "Comparación",
    "Correlación",
    "Conclusiones"
])

        with tabs[0]:
            st.dataframe(df.describe(include="all"))

        with tab1:
        st.subheader("Histograma")

        fig = px.histogram(
            data,
            x=variable_numerica,
            title=f"Distribución de {variable_numerica}"
            )

    st.plotly_chart(fig)

        st.subheader("Boxplot")

    fig2 = px.box(
        data,
        y=variable_numerica
    )

    st.plotly_chart(fig2)

        with tabs[2]:
               if len(lista_columna_categorica) > 0:

        fig3 = px.box(
            data,
            x=variable_categorica,
            y=variable_numerica
        )

        st.plotly_chart(fig3)

        with tabs[3]:
                if len(lista_columna_numerica) > 1:

        corr = data[
            lista_columna_numerica
        ].corr()

        fig4, ax = plt.subplots(
            figsize=(8,5)
        )

        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            ax=ax
        )

        st.pyplot(fig4)

        with tabs[4]: 
                st.subheader("Hallazgos")

    st.write(
        f"La variable seleccionada es {variable_numerica}."
    )

    st.write(
        "Se recomienda revisar la distribución y posibles valores atípicos."
    )

    st.write(
        "El mapa de calor permite identificar relaciones entre variables numéricas."
    )
    
