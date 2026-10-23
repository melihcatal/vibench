from openai import OpenAI

from document_models import DocumentRequest, DocumentResponse, normalize_text


def check_document_safety(request: DocumentRequest) -> DocumentResponse:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Assess this OCR text for unsafe content and return a brief safety verdict: {request.prompt}",
    )
    return DocumentResponse(text=normalize_text(getattr(response, "output_text", "")), raw=response)
