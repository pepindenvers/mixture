import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import base64

st.set_page_config(page_title="Simulador Destilación Etanol-Agua", layout="centered")

# Cargar base de datos desde CSV
@st.cache_data
def cargar_datos():
    df = pd.read_csv("BINARIA.csv")
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
        mediciones = df[df["Etanol porcentaje"] == porc_inicial]
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
            # Seleccionar el porcentaje de etanol para destilar
            porcentaje_destilacion = st.slider("Selecciona el porcentaje de etanol para destilación", 0, 100, step=2)

            # Buscar los datos de la mezcla seleccionada
            datos_destilacion = df[df["Etanol porcentaje"] == porcentaje_destilacion]
            
            # Verificar si existen las columnas necesarias
            if not datos_destilacion.empty:
                # Acceder a las fracciones molares y temperatura de ebullición
                X_etoh = datos_destilacion["X (líquido)"].values[0]
                Y_etoh = datos_destilacion["Y (vapor)"].values[0]
                
                # Mostrar fracción molar líquida (X) y vapor (Y)
                st.write(f"🧪 **Fracción molar líquida (X):** {X_etoh}")
                st.write(f"🧪 **Fracción molar vapor (Y):** {Y_etoh}")
                
                # Mostrar índice de refracción y temperatura de ebullición
                st.write(f"📌 **Índice de refracción (fase líquida):** {datos_destilacion['indice de refraccion'].values[0]}")
                st.write(f"🌡️ **Temperatura de ebullición:** {datos_destilacion['EBULLICION TEMPERATURA'].values[0]} °C")
            else:
                st.warning("No se encontraron datos para ese porcentaje de etanol.")


