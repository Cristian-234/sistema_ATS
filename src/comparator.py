from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Cargamos el modelo preentrenado de Hugging Face.
# La primera vez que corras el script se descargará automáticamente (~90MB).
print("[INFO] Cargando modelo de embeddings de Hugging Face...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_similarity(job_description, resume_text):
    """
    Recibe el texto de la oferta de trabajo y el texto de un CV.
    Genera sus vectores (embeddings) y calcula el porcentaje de similitud matemática.
    """
    # 1. Generar los embeddings (vectores numéricos de 384 dimensiones)
    embeddings = model.encode([job_description, resume_text])
    
    # Separamos los vectores resultantes
    vector_job = embeddings[0].reshape(1, -1)
    vector_resume = embeddings[1].reshape(1, -1)
    
    # 2. Calcular la similitud de coseno entre ambos vectores
    similarity_score = cosine_similarity(vector_job, vector_resume)[0][0]
    
    # Convertimos el resultado (que va de -1 a 1) en un porcentaje limpio del 0 al 100
    percentage_score = float(similarity_score) * 100
    
    # Forzar límites lógicos en caso de valores negativos extraños
    return max(0.0, round(percentage_score, 2))

if __name__ == "__main__":
    # Test de Integración Semántica
    print("\n--- Probando Módulo de Similitud Semántica ---")
    
    # Definimos una oferta de trabajo ejemplo
    oferta_puesto = "We are looking for a Python Software Engineer with experience in building web applications and backend APIs using Django or Flask."
    
    # Simulamos 3 CVs con diferentes niveles de afinidad
    cv_perfecto = "Python Developer specialized in backend systems. Experienced in creating RESTful APIs using Flask and managing databases."
    cv_relacionado = "Software Engineer with background in Java and Spring Boot, but recently working on data pipelines with Python."
    cv_malo = "Graphic designer and UI expert with deep knowledge in Adobe Photoshop, Figma, and creative branding strategies."
    
    print(r"[Oferta de Trabajo]:", oferta_puesto)
    print("-" * 50)
    
    # Evaluamos los CVs
    score_1 = calculate_similarity(oferta_puesto, cv_perfecto)
    score_2 = calculate_similarity(oferta_puesto, cv_relacionado)
    score_3 = calculate_similarity(oferta_puesto, cv_malo)
    
    print(f"-> Score CV Perfecto (Backend/Flask): {score_1}%")
    print(f"-> Score CV Relacionado (Java/Python): {score_2}%")
    print(f"-> Score CV Sin relación (Diseño):     {score_3}%")