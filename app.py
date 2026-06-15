
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="App Analizadora de Datasets", layout="wide")

def load_data(file):
    return pd.read_csv(file)


st.title("📊 App Analizadora de Datasets")

menu = st.sidebar.radio(
    "Menú",
    ["Home","Carga y Perfil","Procesamiento","Análisis Visual"]
)

if "df" not in st.session_state:
    st.session_state.df = None

if menu=="Home":
    st.header("Proyecto Final Integrador")
    st.write("Autor: Yaneri Martinez Huamani")
    st.write("Tecnologías: Python, Pandas, Streamlit, Plotly, Matplotlib, Seaborn, GitHub")
    st.info("Resultados exploratorios.")
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

        num_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()

        cat_cols = df.select_dtypes(
            include="object"
        ).columns.tolist()

        tabs = st.tabs([
            "Resumen",
            "Distribución",
            "Comparación",
            "Correlación",
            "Conclusiones"
        ])

        with tabs[0]:

            st.dataframe(
                df.describe(include="all")
            )
# TAB 2
        with tabs[1]:
        
            if len(num_cols) > 0:
        
                variable_numerica = st.selectbox(
                    "Seleccione una variable numérica",
                    num_cols
                )
        
                st.subheader("Histograma")
        
                fig = px.histogram(
                    df,
                    x=variable_numerica
                )
        
                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
        
                st.subheader("Boxplot")
        
                fig2 = px.box(
                    df,
                    y=variable_numerica
                )
        
                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )
        
        # TAB 3
        with tabs[2]:
        
            if len(num_cols) > 0 and len(cat_cols) > 0:
        
                variable_numerica = st.selectbox(
                    "Variable numérica",
                    num_cols,
                    key="num"
                )
        
                variable_categorica = st.selectbox(
                    "Variable categórica",
                    cat_cols,
                    key="cat"
                )
        
                fig3 = px.box(
                    df,
                    x=variable_categorica,
                    y=variable_numerica
                )
        
                st.plotly_chart(
                    fig3,
                    use_container_width=True
                )
        
        # TAB 4
        with tabs[3]:
        
            if len(num_cols) > 1:
        
                corr = df[num_cols].corr()
        
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
        
        # TAB 5
        with tabs[4]:
        
            st.subheader("Hallazgos")
        
            st.write(
                f"Cantidad de registros: {df.shape[0]}"
            )
        
            st.write(
                f"Cantidad de columnas: {df.shape[1]}"
            )
        
            st.write(
                f"Valores nulos encontrados: {int(df.isna().sum().sum())}"
            )
        
            st.success(
                "Revise los gráficos para identificar distribuciones, valores atípicos y relaciones entre variables."
            )
    
