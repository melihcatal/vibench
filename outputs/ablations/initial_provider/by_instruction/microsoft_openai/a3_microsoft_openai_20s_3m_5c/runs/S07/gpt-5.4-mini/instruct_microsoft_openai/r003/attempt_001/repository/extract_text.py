import base64
from pathlib import Path

from document_client import create_client, load_config
from document_models import DocumentRequest, DocumentResponse, normalize_text


def _to_data_url(path: str) -> str:
    data = Path(path).read_bytes()
    encoded = base64.b64encode(data).decode("ascii")
    suffix = Path(path).suffix.lower().lstrip(".") or "png"
    mime = f"image/{'jpeg' if suffix in ('jpg', 'jpeg') else suffix}"
    return f"data:{mime};base64,{encoded}"


def extract_text(request: DocumentRequest) -> DocumentResponse:
    cfg = load_config()
    client = create_client()
    image_url = request.image_b64 or (_to_data_url(request.image_path) if request.image_path else "")
    response = client.responses.create(
        model=cfg.openai_model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": request.prompt or "Extract plain text from this scanned document image."},
                    {"type": "input_image", "image_url": image_url},
                ],
            }
        ],
    )
    return DocumentResponse(text=normalize_text(getattr(response, "output_text", "")), raw=response)
