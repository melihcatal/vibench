from document_client import create_client, load_config
from document_models import DocumentRequest, DocumentResponse, normalize_text


def extract_layout(request: DocumentRequest) -> DocumentResponse:
    cfg = load_config()
    client = create_client()
    response = client.responses.create(
        model=cfg.openai_model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": request.prompt or "Extract layout elements such as blocks, lines, tables, and reading order as structured JSON."},
                    {"type": "input_image", "image_url": request.image_b64 or ""},
                ],
            }
        ],
    )
    return DocumentResponse(text=normalize_text(getattr(response, "output_text", "")), raw=response)
