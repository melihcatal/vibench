import os

from google.cloud import documentai

from document_client import build_processor_name, get_config, get_document_ai_client
from document_models import DocumentInput, normalize_text


def extract_text(image_bytes: bytes, mime_type: str = "image/png") -> str:
    cfg = get_config()
    client = get_document_ai_client()
    name = build_processor_name(cfg["project_id"], cfg["location"], cfg["processor_id"])
    raw_document = documentai.RawDocument(content=image_bytes, mime_type=mime_type)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)
    response = client.process_document(request=request)
    return normalize_text(response.document.text)


def main() -> None:
    path = os.getenv("DOCUMENT_IMAGE_PATH")
    if not path:
        return
    with open(path, "rb") as f:
        print(extract_text(f.read()))


if __name__ == "__main__":
    main()
