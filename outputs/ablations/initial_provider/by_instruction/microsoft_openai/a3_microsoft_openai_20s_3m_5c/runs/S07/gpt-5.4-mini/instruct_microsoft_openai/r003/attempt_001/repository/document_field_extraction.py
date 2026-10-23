from openai import OpenAI

from document_models import DocumentRequest, DocumentResponse, normalize_text


def extract_document_fields(request: DocumentRequest) -> DocumentResponse:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Extract structured fields from this normalized OCR text as JSON: {request.prompt}",
    )
    return DocumentResponse(text=normalize_text(getattr(response, "output_text", "")), raw=response)
