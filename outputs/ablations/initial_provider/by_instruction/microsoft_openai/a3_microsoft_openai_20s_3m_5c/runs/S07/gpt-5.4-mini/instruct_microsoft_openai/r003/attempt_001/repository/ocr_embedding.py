from openai import OpenAI

from document_models import DocumentRequest, DocumentResponse, normalize_text


def embed_ocr_sections(request: DocumentRequest) -> DocumentResponse:
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=request.prompt,
    )
    return DocumentResponse(text=normalize_text(getattr(response, "data", [])), raw=response)
