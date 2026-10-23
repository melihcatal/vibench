from openai import OpenAI

from document_models import DocumentRequest, DocumentResponse, normalize_text


def translate_ocr_text(request: DocumentRequest, target_language: str) -> DocumentResponse:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate the following OCR text into {target_language}: {request.prompt}",
    )
    return DocumentResponse(text=normalize_text(getattr(response, "output_text", "")), raw=response)
