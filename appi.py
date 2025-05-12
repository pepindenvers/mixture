# Paso 6: Destilación
if st.button("Destilar"):
    # Seleccionar el porcentaje de etanol para destilar
    porcentaje_destilacion = st.slider("Selecciona el porcentaje de etanol para destilación", 0, 100, step=2)
    
    # Buscar los datos de la mezcla seleccionada
    datos_destilacion = df[df["Etanol porcentaje"] == porcentaje_destilacion]
    
    # Mostrar las columnas disponibles en el DataFrame para diagnóstico
    st.write("🔍 Columnas disponibles en el DataFrame:", df.columns.tolist())

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


