import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

st.set_page_config(page_title="Simulador Destilación Etanol-Agua", layout="centered")

# Cargar base de datos desde CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("BINARIA.csv")
    df.columns = df.columns.str.strip()  # Eliminar espacios extra
    df["Etanol porcentaje"] = pd.to_numeric(df["Etanol porcentaje"], errors='coerce')
    df = df.rename(columns={
        "nd indice de refraccion": "indice de refraccion",
        "Temperatura": "EBULLICION TEMPERATURA"
    })
    return df

df = cargar_datos()

st.title("🧪 Simulador de Destilación Etanol-Agua")
st.write("Simulador interactivo para la destilación de mezclas etanol-agua usando datos reales de índice de refracción y fracciones molares.")

# Paso 1: Selección de concentración
porc_inicial = st.slider("Selecciona el porcentaje de etanol inicial en la mezcla", 0, 100, step=2)

if 'etapas' not in st.session_state:
    st.session_state.etapas = []

if st.button("Iniciar medición"):
    file_ = open("alcoho.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="mezcla" style="width: 300px;">',
        unsafe_allow_html=True,
    )
    st.session_state.etapas.append(porc_inicial)

# Mostrar datos medidos
if st.session_state.etapas:
    if st.button("Continuar medición"):
        mediciones = df[df["Etanol porcentaje"] == float(porc_inicial)]
        if not mediciones.empty:
            st.success("Índice de refracción encontrado:")
            st.write(mediciones[["indice de refraccion"]])
        else:
            st.error("Datos no encontrados para ese porcentaje.")

    if st.button("Finalizar"):
        st.subheader("📈 Gráfica de Calibración")
        fig, ax = plt.subplots()
        ax.plot(df["Etanol porcentaje"], df["indice de refraccion"], marker="o")
        ax.set_xlabel("Porcentaje de Etanol (%)")
        ax.set_ylabel("Índice de Refracción")
        ax.set_title("Curva de Calibración")
        st.pyplot(fig)

        if st.button("Destilar"):
            # Mostrar GIF de destilación
            file_ = open("destila.gif", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()
            st.markdown(
                f'<img src="data:image/gif;base64,{data_url}" alt="destilacion" style="width: 300px;">',
                unsafe_allow_html=True,
            )

            # Mostrar tabla resumen de etapas previas
            tabla = df[df["Etanol porcentaje"].isin(st.session_state.etapas)]
            columnas_tabla = ["Etanol porcentaje", "EBULLICION TEMPERATURA"]
            for col in ["Xetoh_liquido", "Xetoh_vapor"]:
                if col in df.columns:
                    columnas_tabla.append(col)
            st.write("🔬 Resultados de Destilación")
            st.dataframe(tabla[columnas_tabla].reset_index(drop=True))

            # Sección interactiva de análisis de mezcla
            st.subheader("🔍 Seleccionar mezcla para analizar")
            porcentajes_disponibles = sorted(df["Etanol porcentaje"].dropna().unique())
            mezcla_seleccionada = st.selectbox("Selecciona el porcentaje de etanol:", porcentajes_disponibles)

            datos_mezcla = df[df["Etanol porcentaje"] == mezcla_seleccionada]

            if not datos_mezcla.empty:
                indice = datos_mezcla["indice de refraccion"].values[0]
                temp = datos_mezcla["EBULLICION TEMPERATURA"].values[0]
                st.write(f"📌 **Índice de refracción:** {indice}")
                st.write(f"🌡️ **Temperatura de ebullición:** {temp} °C")
            else:
                st.warning("No se encontraron datos para ese porcentaje.")


