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

# Paso 1: Mostrar gráfica de calibración
st.subheader("📈 Curva de Calibración")
columna_ir = [col for col in df.columns if "refrac" in col.lower()]
if columna_ir:
    fig, ax = plt.subplots()
    ax.plot(df["Etanol porcentaje"], df[columna_ir[0]], marker="o")
    ax.set_xlabel("Porcentaje de Etanol (%)")
    ax.set_ylabel("Índice de Refracción")
    ax.set_title("Curva de Calibración")
    st.pyplot(fig)

# Paso 2: Selección del porcentaje de etanol
porc_inicial = st.slider("Selecciona el porcentaje de etanol inicial en la mezcla", 0, 100, step=2)

# Paso 3: Mostrar botón para iniciar medición
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

# Paso 4: Mostrar datos de la mezcla seleccionada
if st.session_state.etapas:
    if st.button("Ver datos de la mezcla"):
        mediciones = df[df["Etanol porcentaje"] == float(porc_inicial)]
        
        # Verificar si existen las columnas necesarias
        columna_ir = [col for col in df.columns if "refrac" in col.lower()]
        columna_temp = [col for col in df.columns if "temp" in col.lower()]

        if not mediciones.empty:
            if columna_ir:
                st.write(f"📌 **Índice de refracción:** {mediciones[columna_ir[0]].values[0]}")
            if columna_temp:
                st.write(f"🌡️ **Temperatura de ebullición:** {mediciones[columna_temp[0]].values[0]} °C")
        else:
            st.warning("No se encontraron datos para ese porcentaje.")

