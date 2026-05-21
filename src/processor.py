import spacy
import re

def cargar_modelo_spacy(idioma="Español"):
    try:
        if idioma == "Español":
            return spacy.load("es_core_news_sm")
        else:
            return spacy.load("en_core_web_sm")
    except OSError as e:
        raise OSError("El modelo requerido no está instalado. Ejecuta: python -m spacy download es_core_news_sm") from e

# Cargamos el modelo por defecto (Español)
nlp = cargar_modelo_spacy()

def clean_and_lemmatize(text):  
    """
    Limpia el texto: elimina caracteres especiales, pasa a minúsculas,
    remueve stopwords y convierte cada palabra a su lema (raíz).
    """
    # 1. Limpieza básica con expresiones regulares (quitar URLs, correos y caracteres extraños)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) # Quita URLs
    text = re.sub(r'\S+@\S+', '', text) # Quita correos electrónicos
    text = re.sub(r'[^a-zA-Z\s]', ' ', text) # Quita números y caracteres especiales (deja solo letras)
    
    # 2. Procesamiento con spaCy
    doc = nlp(text.lower()) # Pasamos a minúsculas y procesamos con el modelo
    
    cleaned_tokens = []
    for token in doc:
        # Filtramos: que no sea stopword, que no sea espacio en blanco y que tenga longitud válida
        if not token.is_stop and not token.is_space and len(token.text) > 1:
            cleaned_tokens.append(token.lemma_) # Guardamos el lema (raíz) de la palabra
            
    # Unimos los tokens limpios en una sola cadena de texto
    return " ".join(cleaned_tokens)

def extract_named_entities(text):
    """
    Extrae entidades nombradas del texto original (como Organizaciones o Lugares)
    para identificar posibles universidades o empresas pasadas.
    """
    doc = nlp(text)
    entities = {"organizations": [], "locations": []}
    
    for ent in doc.ents:
        if ent.label_ == "ORG" and ent.text not in entities["organizations"]:
            entities["organizations"].append(ent.text)
        elif ent.label_ in ["GPE", "LOC"] and ent.text not in entities["locations"]:
            entities["locations"].append(ent.text)
            
    return entities

if __name__ == "__main__":
    # Test rápido de funcionamiento
    print("--- Probando Módulo de Procesamiento NLP ---")
    
    texto_sucio_prueba = """
    John Doe - Software Engineer at Google Inc.
    Contact: john.doe@email.com | Website: https://johndoe.dev
    I have been developing complex web applications for over 5 years using Python, 
    JavaScript, and cloud services. I loved working with agile teams.
    """
    
    print("\n[Texto Original]:")
    print(texto_sucio_prueba.strip())
    
    print("\n[Texto Limpio y Lematizado]:")
    texto_limpio = clean_and_lemmatize(texto_sucio_prueba)
    print(texto_limpio)
    
    print("\n[Entidades Detectadas]:")
    entidades = extract_named_entities(texto_sucio_prueba)
    print(entidades)