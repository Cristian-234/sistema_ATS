import re

import spacy


def cargar_modelo_spacy(idioma="Espanol"):
    """
    Carga el modelo de spaCy segun el idioma seleccionado por el usuario.
    """
    try:
        normalized_language = idioma.lower().replace("ñ", "n")
        if normalized_language in ("espanol", "spanish"):
            return spacy.load("es_core_news_sm")
        return spacy.load("en_core_web_sm")
    except OSError as exc:
        raise OSError(
            "El modelo requerido no esta instalado. "
            "Ejecuta: python -m spacy download es_core_news_sm "
            "o python -m spacy download en_core_web_sm"
        ) from exc


nlp = cargar_modelo_spacy()


def clean_and_lemmatize(text, nlp_model=None):
    """
    Limpia el texto, elimina ruido y lematiza sin destruir terminos tecnicos.
    """
    active_nlp = nlp_model or nlp

    text = re.sub(r"http\S+|www\S+|https\S+", " ", text, flags=re.MULTILINE)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    doc = active_nlp(text.lower())

    cleaned_tokens = []
    for token in doc:
        if token.is_stop or token.is_space or token.is_punct:
            continue
        if len(token.text.strip()) <= 1:
            continue
        cleaned_tokens.append(token.lemma_)

    return " ".join(cleaned_tokens)


def extract_named_entities(text, nlp_model=None):
    """
    Extrae entidades nombradas del texto original.
    """
    active_nlp = nlp_model or nlp
    doc = active_nlp(text)
    entities = {"organizations": [], "locations": []}

    for ent in doc.ents:
        if ent.label_ == "ORG" and ent.text not in entities["organizations"]:
            entities["organizations"].append(ent.text)
        elif ent.label_ in ["GPE", "LOC"] and ent.text not in entities["locations"]:
            entities["locations"].append(ent.text)

    return entities


if __name__ == "__main__":
    texto_prueba = """
    Software Engineer con experiencia en Python, REST APIs, SQL, Docker y AWS.
    Contacto: ejemplo@email.com | Sitio: https://portfolio.dev
    """

    print("--- Probando modulo de procesamiento NLP ---")
    print(clean_and_lemmatize(texto_prueba))
    print(extract_named_entities(texto_prueba))
