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

# Paso 1: Selección del porcentaje de etanol
porc_inicial = st.slider("Selecciona el porcentaje de etanol inicial en la mezcla", 0, 100, step=2)

# Paso 2: Mostrar índice de refracción para el porcentaje seleccionado
if st.button("Mostrar índice de refracción"):
    mediciones = df[df["Etanol porcentaje"] == porc_inicial]
    if not mediciones.empty:
        st.write(f"📌 **Índice de refracción:** {mediciones['indice de refraccion'].values[0]}")
    else:
        st.warning("No se encontraron datos para ese porcentaje.")

# Paso 3: Iniciar medición y registrar los resultados
if 'etapas' not in st.session_state:
    st.session_state.etapas = []

if st.button("Iniciar medición"):
    st.session_state.etapas.append(porc_inicial)
    st.write(f"🌡️ Mediciones registradas: {len(st.session_state.etapas)}")
    st.write(f"Porcentaje de etanol: {porc_inicial}%")

# Paso 4: Continuar medición
if st.session_state.etapas:
    if st.button("Continuar medición"):
        st.write(f"📌 Mediciones registradas: {len(st.session_state.etapas)}")
        st.write(f"Última medición: {st.session_state.etapas[-1]}% de etanol")
    
    # Mostrar la tabla de mediciones realizadas
    tabla_mediciones = pd.DataFrame({"% Etanol": st.session_state.etapas})
    st.write("🔬 Mediciones realizadas:")
    st.write(tabla_mediciones)

# Paso 5: Mostrar curva de calibración cuando el usuario finaliza
if st.button("Finalizar medición"):
    st.subheader("📈 Curva de Calibración")
    fig, ax = plt.subplots()
    ax.plot(df["Etanol porcentaje"], df["indice de refraccion"], marker="o")
    ax.set_xlabel("Porcentaje de Etanol (%)")
    ax.set_ylabel("Índice de Refracción")
    ax.set_title("Curva de Calibración")
    st.pyplot(fig)

# Paso 6: Destilación
if st.button("Destilar"):
    # Seleccionar el porcentaje de etanol para destilar
    porcentaje_destilacion = st.slider("Selecciona el porcentaje de etanol para destilación", 0, 100, step=2)
    
    # Buscar los datos de la mezcla seleccionada
    datos_destilacion = df[df["Etanol porcentaje"] == porcentaje_destilacion]
    
    # Verificar si existen las columnas necesarias
    columna_ir = [col for col in df.columns if "refrac" in col.lower()]
    columna_temp = [col for col in df.columns if "temp" in col.lower()]

    if not datos_destilacion.empty:
        if columna_ir:
            st.write(f"📌 **Índice de refracción (fase líquida):** {datos_destilacion[columna_ir[0]].values[0]}")
        if columna_temp:
            st.write(f"🌡️ **Temperatura de ebullición:** {datos_destilacion[columna_temp[0]].values[0]} °C")
        
        # Fase vapor y fase líquida
        X_etoh = datos_destilacion["Xetoh_liquido"].values[0]
        Y_etoh = datos_destilacion["Xetoh_vapor"].values[0]
        st.write(f"🧪 **Fracción molar líquida (X):** {X_etoh}")
        st.write(f"🧪 **Fracción molar vapor (Y):** {Y_etoh}")
    else:
        st.warning("No se encontraron datos para ese porcentaje de etanol.")

