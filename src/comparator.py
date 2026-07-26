from functools import lru_cache

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


AVAILABLE_MODELS = {
    "Multilingue MiniLM L12": "paraphrase-multilingual-MiniLM-L12-v2",
    "MiniLM L6 Ingles": "all-MiniLM-L6-v2",
    "DistilUSE Multilingue": "distiluse-base-multilingual-cased-v2",
}

DEFAULT_MODEL_LABEL = "Multilingue MiniLM L12"


@lru_cache(maxsize=3)
def load_embedding_model(model_name):
    print(f"[INFO] Cargando modelo de embeddings: {model_name}")
    return SentenceTransformer(model_name)


def calculate_similarity(job_description, resume_text, model_name=None):
    """
    Genera embeddings para la oferta y el CV, y retorna similitud de coseno.
    """
    selected_model = model_name or AVAILABLE_MODELS[DEFAULT_MODEL_LABEL]
    model = load_embedding_model(selected_model)

    embeddings = model.encode([job_description, resume_text])
    vector_job = embeddings[0].reshape(1, -1)
    vector_resume = embeddings[1].reshape(1, -1)

    similarity_score = cosine_similarity(vector_job, vector_resume)[0][0]
    percentage_score = float(similarity_score) * 100

    return max(0.0, min(100.0, round(percentage_score, 2)))


def compare_embedding_models(job_description, resume_text, model_labels=None):
    """
    Calcula el score del mismo par oferta-CV con varios modelos.
    """
    labels = model_labels or list(AVAILABLE_MODELS.keys())
    results = {}

    for label in labels:
        model_name = AVAILABLE_MODELS[label]
        results[label] = calculate_similarity(job_description, resume_text, model_name)

    return results


if __name__ == "__main__":
    oferta = "Python Software Engineer with experience building backend APIs using Flask."
    cv = "Backend developer specialized in Python, REST APIs, Flask and SQL databases."

    print("--- Probando similitud semantica ---")
    print(calculate_similarity(oferta, cv))
