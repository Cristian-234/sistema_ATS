import os

import pdfplumber


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a digital PDF while preserving line breaks.
    Preserving lines helps downstream section detection.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo no existe en la ruta: {pdf_path}")

    pages_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                pages_text.append(_normalize_lines(text))
            else:
                print(
                    f"[Advertencia] La pagina {page_number} de {pdf_path} "
                    "no contiene texto extraible."
                )

    return "\n".join(pages_text).strip()


def _normalize_lines(text):
    lines = []
    for line in text.splitlines():
        cleaned_line = " ".join(line.split())
        if cleaned_line:
            lines.append(cleaned_line)
    return "\n".join(lines)


if __name__ == "__main__":
    test_pdf = "sample_accountant_cv_clear_sections.pdf"

    if os.path.exists(test_pdf):
        extracted_text = extract_text_from_pdf(test_pdf)
        print("--- Probando extractor de PDF ---")
        print(f"Caracteres extraidos: {len(extracted_text)}")
        print(extracted_text[:500] + "...")
    else:
        print(f"Coloca un PDF de prueba en '{test_pdf}' para ejecutar el test.")
