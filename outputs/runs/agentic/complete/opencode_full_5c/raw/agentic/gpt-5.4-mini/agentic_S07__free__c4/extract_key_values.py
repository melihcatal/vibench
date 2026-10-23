from google.cloud import vision

from document_client import normalize_kv_pairs, vision_client
from document_models import DocumentRequest, KeyValueResponse


def extract_key_values(request: DocumentRequest) -> KeyValueResponse:
    client = vision_client()
    with open(request.image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    result = client.document_text_detection(image=image)
    pairs = []
    if result.full_text_annotation:
        for page in result.full_text_annotation.pages:
            for block in page.blocks:
                text = " ".join(
                    symbol.text
                    for paragraph in block.paragraphs
                    for word in paragraph.words
                    for symbol in word.symbols
                )
                if ":" in text:
                    key, value = text.split(":", 1)
                    pairs.append({"key": key.strip(), "value": value.strip()})
    return KeyValueResponse(pairs=normalize_kv_pairs(pairs))
