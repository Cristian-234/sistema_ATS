import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    """
    Abre un archivo PDF y extrae todo su contenido de texto de forma secuencial.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo no existe en la ruta: {pdf_path}")
        
    full_text = []
    
    # Abrimos el PDF de manera segura usando un manejador de contexto (with)
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:  # Si la página no está vacía (o no es solo una imagen)
                full_text.append(text)
            else:
                print(f"[Advertencia] La página {i+1} de {pdf_path} no contiene texto extraíble.")
                
    # Unimos todas las páginas con un salto de línea y limpiamos espacios extra
    cleaned_text = "\n".join(full_text)
    return " ".join(cleaned_text.split())

if __name__ == "__main__":
    # Script de prueba rápida (Sanity Check)
    # Pon un PDF de prueba en tu carpeta data/resumes/ y escribe su nombre aquí para probarlo
    test_pdf = "data/resumes/prueba.pdf"
    
    if os.path.exists(test_pdf):
        print("--- Probando Extractor de PDF ---")
        texto_extraido = extract_text_from_pdf(test_pdf)
        print(f"Caracteres extraídos: {len(texto_extraido)}")
        print("\nPrimeros 300 caracteres del texto:")
        print(texto_extraido[:300] + "...")
    else:
        print(f"Coloca un PDF de prueba en '{test_pdf}' para ejecutar el test automático.")