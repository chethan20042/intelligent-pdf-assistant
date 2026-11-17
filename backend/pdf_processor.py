
import pymupdf
import os


def extract_text_from_pdf(pdf_path):

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    document = pymupdf.open(pdf_path)

    extracted_pages = []

    for page_number, page in enumerate(document, start=1):

        text = page.get_text("text").strip()

        if text:
            extracted_pages.append({
                "page": page_number,
                "text": text
            })

    document.close()

    return extracted_pages
