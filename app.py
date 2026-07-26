import os
import tempfile

import pandas as pd
import streamlit as st

from src.analyzer import extract_resume_sections, extract_skills, get_available_domains
from src.comparator import (
    AVAILABLE_MODELS,
    DEFAULT_MODEL_LABEL,
    calculate_similarity,
    compare_embedding_models,
)
from src.extractor import extract_text_from_pdf
from src.processor import cargar_modelo_spacy, clean_and_lemmatize
from src.scoring import build_explanation, calculate_section_scores, calculate_weighted_score


st.set_page_config(
    page_title="ATS Inteligente - Ranking Semantico",
    page_icon="ATS",
    layout="wide",
)


DOMAIN_LABELS = {
    "Technology / Software": "Tecnologia / Software",
    "Accounting / Finance": "Contabilidad / Finanzas",
    "Healthcare": "Salud",
    "Education": "Educacion",
    "Marketing / Sales": "Marketing / Ventas",
    "Human Resources": "Recursos Humanos",
    "Operations / Logistics": "Operaciones / Logistica",
}


DOMAIN_EXAMPLES = {
    "Technology / Software": {
        "title": "Desarrollador Python Senior",
        "description": (
            "Buscamos un ingeniero de software con experiencia en Python, APIs REST, SQL, "
            "Docker, servicios cloud y metodologias agiles."
        ),
    },
    "Accounting / Finance": {
        "title": "Contador Senior",
        "description": (
            "Buscamos un contador con experiencia en conciliacion bancaria, estados financieros, "
            "IGV, impuesto a la renta, SAP FI, Excel y reportes bajo NIIF."
        ),
    },
    "Healthcare": {
        "title": "Enfermero Registrado",
        "description": (
            "Buscamos un profesional de salud con experiencia en atencion al paciente, signos vitales, "
            "triaje, historias clinicas, administracion de medicamentos y control de infecciones."
        ),
    },
    "Education": {
        "title": "Docente de Ingles",
        "description": (
            "Buscamos un docente con experiencia en planificacion de clases, manejo de aula, "
            "evaluacion de estudiantes, tutorias, plataformas LMS y educacion virtual."
        ),
    },
    "Marketing / Sales": {
        "title": "Especialista en Marketing Digital",
        "description": (
            "Buscamos un especialista con experiencia en marketing digital, SEO, redes sociales, "
            "Google Analytics, generacion de leads, CRM y reportes de campanas."
        ),
    },
    "Human Resources": {
        "title": "Generalista de Recursos Humanos",
        "description": (
            "Buscamos un profesional de recursos humanos con experiencia en reclutamiento, entrevistas, "
            "onboarding, planilla, legislacion laboral, capacitacion y evaluacion de desempeno."
        ),
    },
    "Operations / Logistics": {
        "title": "Coordinador de Logistica",
        "description": (
            "Buscamos un coordinador logistico con experiencia en gestion de inventarios, almacenes, "
            "cadena de suministro, compras, transporte y reportes de KPI."
        ),
    },
}


def inject_css():
    st.markdown(
        """
    
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        [data-testid="stSidebar"] label {
            color: #dbeafe !important;
            font-weight: 650;
        }

        [data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background-color: #1e293b !important;
            border: 1px solid #334155 !important;
            color: #f8fafc !important;
        }

        [data-testid="stSidebar"] div[data-baseweb="select"] span {
            color: #f8fafc !important;
        }

        [data-testid="stSidebar"] input {
            color: #f8fafc !important;
        }
        [data-testid="stSidebar"] svg {
            color: #f8fafc !important;
            fill: #f8fafc !important;
        }

        .ats-hero {
            padding: 28px 30px;
            border-radius: 14px;
            background:
                linear-gradient(135deg, rgba(37, 99, 235, 0.96), rgba(8, 145, 178, 0.92)),
                #2563eb;
            color: white;
            margin-bottom: 22px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.16);
        }

        .ats-hero h1 {
            margin: 0 0 8px 0;
            font-size: 34px;
            line-height: 1.15;
            letter-spacing: 0;
        }

        .ats-hero p {
            margin: 0;
            color: #e0f2fe;
            font-size: 16px;
            max-width: 940px;
        }

        .ats-note {
            border-left: 4px solid #2563eb;
            padding: 10px 12px;
            background: #eff6ff;
            color: #1e3a8a;
            border-radius: 6px;
            margin: 12px 0 18px 0;
        }

        .score-pill {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            font-weight: 700;
            color: white;
            background: #2563eb;
        }

        .stButton > button {
            width: 100%;
            border-radius: 8px;
            min-height: 46px;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            border: 1px solid #dbe4f0;
            border-radius: 10px;
            padding: 14px 16px;
            background: #f8fafc;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"],
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #0f172a !important;
        }

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-weight: 800;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner=False)
def get_spacy_model(language):
    return cargar_modelo_spacy(language)


def format_list(values):
    if not values:
        return "No detectado"
    return ", ".join(values)


def get_domain_example(domain):
    return DOMAIN_EXAMPLES.get(domain, DOMAIN_EXAMPLES["Accounting / Finance"])


def render_hero():
    st.markdown(
        """
        <div class="ats-hero">
            <h1>ATS Inteligente: Ranking Semantico de Curriculums</h1>
            <p>
                Sistema multi-area para clasificar CVs mediante NLP, embeddings semanticos,
                taxonomias de habilidades, scoring por secciones y explicabilidad del resultado.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


inject_css()

st.sidebar.title("Configuracion del ATS")

domains = get_available_domains()
default_domain = "Accounting / Finance"
default_domain_index = domains.index(default_domain) if default_domain in domains else 0

domain_selected = st.sidebar.selectbox(
    "Area de la vacante",
    domains,
    index=default_domain_index,
    format_func=lambda domain: DOMAIN_LABELS.get(domain, domain),
)

idioma_seleccionado = st.sidebar.selectbox(
    "Idioma principal",
    ["Espanol", "Ingles"],
)

modelo_label = st.sidebar.selectbox(
    "Modelo de embeddings",
    list(AVAILABLE_MODELS.keys()),
    index=list(AVAILABLE_MODELS.keys()).index(DEFAULT_MODEL_LABEL),
)

activar_secciones = st.sidebar.toggle(
    "Scoring por secciones",
    value=True,
)

activar_comparacion_modelos = st.sidebar.toggle(
    "Comparar modelos para el mejor candidato",
    value=False,
)

nlp = get_spacy_model(idioma_seleccionado)
embedding_model_name = AVAILABLE_MODELS[modelo_label]
example = get_domain_example(domain_selected)

st.sidebar.markdown("---")
st.sidebar.caption(f"Modelo spaCy cargado: {idioma_seleccionado}")
st.sidebar.caption(f"Area activa: {DOMAIN_LABELS.get(domain_selected, domain_selected)}")

render_hero()

top_metrics = st.columns(4)
top_metrics[0].metric("Dominio activo", DOMAIN_LABELS.get(domain_selected, domain_selected))
top_metrics[1].metric("Modelo de incrustacion", modelo_label)
top_metrics[2].metric("Puntuacion de secciones", "Activa" if activar_secciones else "Inactiva")
top_metrics[3].metric("Lote de curriculums", "Carga de PDF")

st.markdown(
    '<div class="ats-note">Para mejores resultados, carga PDFs digitales con texto seleccionable. '
    'Encabezados claros como Experiencia, Habilidades, Educacion y Certificaciones mejoran el scoring por secciones.</div>',
    unsafe_allow_html=True,
)

input_col, upload_col = st.columns([1.1, 0.9], gap="large")

with input_col:
    with st.container(border=True):
        st.markdown("### 1. Configurar oferta de trabajo")
        job_title = st.text_input(
            "Titulo del puesto",
            placeholder=f"Ej. {example['title']}",
        )
        job_description = st.text_area(
            "Descripcion del puesto / requisitos",
            height=260,
            placeholder=example["description"],
        )

with upload_col:
    with st.container(border=True):
        st.markdown("### 2. Cargar curriculums de candidatos")
        uploaded_files = st.file_uploader(
            "Curriculums en PDF",
            type=["pdf"],
            accept_multiple_files=True,
        )
        if uploaded_files:
            st.success(f"{len(uploaded_files)} archivo(s) listo(s) para analizar.")
        else:
            st.info("Agrega uno o mas CVs digitales en PDF para iniciar el ranking.")

run_analysis = st.button("Ejecutar ranking semantico de candidatos", type="primary")

if run_analysis:
    if not job_description.strip():
        st.error("Por favor, ingresa la descripcion del puesto antes de ejecutar el analisis.")
    elif not uploaded_files:
        st.error("Por favor, carga al menos un curriculum en PDF.")
    else:
        st.subheader("Resultados del ranking")

        results = []
        detail_results = {}

        cleaned_job = clean_and_lemmatize(job_description, nlp)
        job_skill_data = extract_skills(job_description, domain_selected)
        job_skills = job_skill_data["flat"]

        with st.expander("Habilidades requeridas detectadas en la oferta", expanded=True):
            st.write(format_list(job_skills))

        progress_bar = st.progress(0)
        status_text = st.empty()

        for index, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Procesando: {uploaded_file.name}...")
            temp_path = None

            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_path = temp_file.name

                raw_text = extract_text_from_pdf(temp_path)
                cleaned_resume = clean_and_lemmatize(raw_text, nlp)

                semantic_score = calculate_similarity(
                    cleaned_job,
                    cleaned_resume,
                    embedding_model_name,
                )

                resume_skill_data = extract_skills(raw_text, domain_selected)
                resume_sections = extract_resume_sections(raw_text)
                section_scores = {}

                if activar_secciones:
                    section_scores = calculate_section_scores(
                        cleaned_job,
                        resume_sections,
                        embedding_model_name,
                    )

                score_data = calculate_weighted_score(
                    semantic_score=semantic_score,
                    job_skills=job_skills,
                    resume_skills=resume_skill_data["flat"],
                    section_scores=section_scores,
                )
                explanation = build_explanation(score_data)

                results.append(
                    {
                        "Candidato": uploaded_file.name,
                        "Score final (%)": score_data["final_score"],
                        "Semantica (%)": score_data["semantic_score"],
                        "Skills (%)": score_data["skill_score"]
                        if score_data["skill_score"] is not None
                        else "N/A",
                        "Secciones (%)": score_data["section_score"]
                        if score_data["section_score"] is not None
                        else "N/A",
                        "Coincidencias clave": explanation["coincidencias"],
                        "Brechas detectadas": explanation["brechas"],
                    }
                )

                detail_results[uploaded_file.name] = {
                    "raw_text": raw_text,
                    "cleaned_text": cleaned_resume,
                    "skills_by_category": resume_skill_data["by_category"],
                    "section_scores": section_scores,
                    "explanation": explanation,
                    "score_data": score_data,
                }

            except Exception as exc:
                st.warning(f"No se pudo procesar {uploaded_file.name}. Error: {exc}")
            finally:
                if temp_path and os.path.exists(temp_path):
                    os.unlink(temp_path)

            progress_bar.progress((index + 1) / len(uploaded_files))

        status_text.text("Procesamiento completado.")

        if results:
            df = pd.DataFrame(results)
            df = df.sort_values(by="Score final (%)", ascending=False).reset_index(drop=True)

            best_candidate = df.iloc[0]["Candidato"]
            best_score = float(df.iloc[0]["Score final (%)"])
            best_details = detail_results[best_candidate]

            summary_cols = st.columns(4)
            summary_cols[0].metric("Mejor candidato", best_candidate)
            summary_cols[1].metric("Score final", f"{best_score:.2f}%")
            summary_cols[2].metric(
                "Score de skills",
                f"{best_details['score_data']['skill_score']}%"
                if best_details["score_data"]["skill_score"] is not None
                else "N/A",
            )
            summary_cols[3].metric(
                "Score por secciones",
                f"{best_details['score_data']['section_score']}%"
                if best_details["score_data"]["section_score"] is not None
                else "N/A",
            )

            st.dataframe(df, use_container_width=True, hide_index=True)

            st.markdown(
                f'<span class="score-pill">Recomendado: {best_candidate} - {best_score:.2f}% de compatibilidad</span>',
                unsafe_allow_html=True,
            )

            st.subheader("Explicabilidad por candidato")
            selected_candidate = st.selectbox(
                "Selecciona un candidato para inspeccionar",
                df["Candidato"].tolist(),
            )

            details = detail_results[selected_candidate]
            st.write(details["explanation"]["resumen"])

            tab_skills, tab_sections, tab_models = st.tabs(
                ["Skills detectadas", "Scores por seccion", "Comparacion de modelos"]
            )

            with tab_skills:
                skill_rows = [
                    {"Categoria": category, "Skills detectadas": format_list(skills)}
                    for category, skills in details["skills_by_category"].items()
                ]
                st.dataframe(pd.DataFrame(skill_rows), use_container_width=True, hide_index=True)

            with tab_sections:
                if details["section_scores"]:
                    section_df = pd.DataFrame(
                        [
                            {"Seccion": section.title(), "Similitud (%)": score}
                            for section, score in details["section_scores"].items()
                        ]
                    )
                    st.dataframe(section_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No se detectaron secciones evaluables en el curriculum.")

            with tab_models:
                if activar_comparacion_modelos:
                    model_scores = compare_embedding_models(cleaned_job, details["cleaned_text"])
                    model_df = pd.DataFrame(
                        [
                            {"Modelo": label, "Similitud (%)": score}
                            for label, score in model_scores.items()
                        ]
                    )
                    st.dataframe(model_df, use_container_width=True, hide_index=True)
                else:
                    st.info("Activa la comparacion de modelos en la barra lateral para ejecutar este analisis.")
