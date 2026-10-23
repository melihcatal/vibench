from document_client import image_from_content, vision_client
from document_models import DocumentRequest, normalize_text


def extract_key_values(request: DocumentRequest) -> dict[str, str]:
    client = vision_client()
    response = client.document_text_detection(image=image_from_content(request.content))
    pairs: dict[str, str] = {}
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            text = normalize_text(" ".join(word.symbols[0].text for para in block.paragraphs for word in para.words if word.symbols))
            if ":" in text:
                key, value = text.split(":", 1)
                pairs[normalize_text(key)] = normalize_text(value)
    return pairs
