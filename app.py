import streamlit as st
import pandas as pd
import tempfile
import os
import streamlit as st

# Importamos las funciones que programamos en los pasos anteriores
from src.extractor import extract_text_from_pdf
from src.processor import clean_and_lemmatize
from src.comparator import calculate_similarity
from src.processor import cargar_modelo_spacy



# Configuración de la página en el navegador
st.set_page_config(
    page_title="ATS Inteligente - Filtro de CVs", 
    page_icon="💼", 
    layout="wide"
)

# 1. Crear el selector en la barra lateral
st.sidebar.title("Configuración Global")
idioma_seleccionado = st.sidebar.selectbox(
    "Selecciona el idioma del Dataset/CVs:",
    ["Español", "Inglés"]
)

# 2. Cargar el modelo correspondiente dinámicamente
nlp = cargar_modelo_spacy(idioma_seleccionado)

st.sidebar.success(f"Modelo cargado: {idioma_seleccionado}")

# Encabezado principal de la aplicación
st.title("💼 Sistema ATS Inteligente: Clasificación de Currículums")
st.markdown("""
Esta herramienta utiliza Procesamiento de Lenguaje Natural (NLP) y Embeddings para analizar 
la compatibilidad semántica entre ofertas de trabajo y postulantes en formato PDF.
""")

st.write("---")

# Creamos una estructura de dos columnas para la interfaz
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 1. Configurar Oferta de Trabajo")
    job_title = st.text_input("Título del Puesto", placeholder="Ej. Senior Python Developer")
    job_description = st.text_area(
        "Descripción del Puesto / Requisitos (En inglés para el dataset de Kaggle)", 
        height=300,
        placeholder="We are looking for a Software Engineer with strong Python background, experience with cloud APIs, SQL and agile frameworks..."
    )

with col2:
    st.subheader("📂 2. Cargar Currículums (PDFs)")
    uploaded_files = st.file_uploader(
        "Arrastra aquí los archivos PDF descargados de Kaggle", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(r"¡Archivos cargados con éxito!")

st.write("---")

# Botón de acción para arrancar el procesamiento de la IA
if st.button("🚀 Iniciar Análisis Semántico", type="primary"):
    # Validaciones rápidas de seguridad
    if not job_description.strip():
        st.error("Por favor, ingresa la descripción del puesto de trabajo.")
    elif not uploaded_files:
        st.error("Por favor, sube al menos un archivo PDF para evaluar.")
    else:
        st.subheader("📊 Resultados del Ranking")
        
        # Lista para almacenar los resultados del procesamiento
        results = []
        
        # 1. Preprocesar la oferta de trabajo una sola vez para ahorrar cómputo
        cleaned_job = clean_and_lemmatize(job_description)
        
        # Barra de progreso visual para el reclutador
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Iterar sobre cada PDF subido
        for index, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Procesando: {uploaded_file.name}...")
            
            try:
                # Streamlit maneja archivos en memoria, así que creamos un archivo temporal en disco
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_path = temp_file.name
                
                # ETIQUETA 1: Extraer el texto bruto
                raw_text = extract_text_from_pdf(temp_path)
                
                # ETIQUETA 2: Limpieza NLP con spaCy
                cleaned_resume = clean_and_lemmatize(raw_text)
                
                # ETIQUETA 3: Medir similitud con Hugging Face
                score = calculate_similarity(cleaned_job, cleaned_resume)
                
                # Almacenar datos finales para la tabla
                results.append({
                    "Candidato (Archivo)": uploaded_file.name,
                    "Compatibilidad (%)": score
                })
                
                # Eliminar archivo temporal de la computadora
                os.unlink(temp_path)
                
            except Exception as e:
                st.warning(f"No se pudo procesar {uploaded_file.name}. Error: {str(e)}")
            
            # Actualizar barra de progreso dinámicamente
            progress_bar.progress((index + 1) / len(uploaded_files))
            
        status_text.text("¡Procesamiento completado con éxito!")
        
        # Convertir resultados a un DataFrame de Pandas para ordenarlos y mostrarlos
        if results:
            df = pd.DataFrame(results)
            # Ordenar de mayor a menor compatibilidad
            df = df.sort_values(by="Compatibilidad (%)", ascending=False).reset_index(drop=True)
            
            # Formatear el score de forma más estética
            df["Compatibilidad (%)"] = df["Compatibilidad (%)"].map("{:.2f}%".format)
            
            # Mostrar tabla interactiva en el Dashboard
            st.dataframe(df, use_container_width=True)
            
            # Resaltar al mejor candidato de la lista
            mejor_candidato = df.iloc[0]["Candidato (Archivo)"]
            mejor_score = df.iloc[0]["Compatibilidad (%)"]
            st.balloons()
            st.info(f"🏆 **Recomendación del sistema:** El candidato **{mejor_candidato}** es el más apto con un **{mejor_score}** de afinidad.")