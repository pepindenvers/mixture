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
    return df

df = cargar_datos()

# Mostrar columnas reales para diagnóstico
st.write("🧾 Columnas detectadas en el archivo CSV:")
st.write(df.columns.tolist())

st.title("🧪 Simulador de Destilación Etanol-Agua")
st.write("Simulador interactivo para la destilación de mezclas etanol-agua usando datos reales de índice de refracción y fracciones molares.")

# Botón "Destilar" desde el principio
if st.button("Destilar"):
    # Mostrar GIF de destilación cuando se hace clic en el botón
    file_ = open("destila.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="destilacion" style="width: 300px;">',
        unsafe_allow_html=True,
    )

    # Mostrar un selectbox para seleccionar el porcentaje de etanol
    st.subheader("🔍 Seleccionar mezcla para analizar")
    porcentajes_disponibles = sorted(df["Etanol porcentaje"].dropna().unique())
    mezcla_seleccionada = st.selectbox("Selecciona el porcentaje de etanol:", porcentajes_disponibles)

    # Filtrar los datos para la mezcla seleccionada
    datos_mezcla = df[df["Etanol porcentaje"] == mezcla_seleccionada]
    
    # Verificar si existen las columnas necesarias
    columna_ir = [col for col in df.columns if "refrac" in col.lower()]
    columna_temp = [col for col in df.columns if "temp" in col.lower()]

    # Mostrar los datos de la mezcla seleccionada
    if not datos_mezcla.empty:
        if columna_ir:
            st.write(f"📌 **Índice de refracción:** {datos_mezcla[columna_ir[0]].values[0]}")
        if columna_temp:
            st.write(f"🌡️ **Temperatura de ebullición:** {datos_mezcla[columna_temp[0]].values[0]} °C")
    else:
        st.warning("No se encontraron datos para ese porcentaje.")
