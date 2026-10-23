from document_client import image_from_content, vision_client
from document_models import DocumentRequest, normalize_text


def extract_layout(request: DocumentRequest) -> list[dict]:
    client = vision_client()
    response = client.document_text_detection(image=image_from_content(request.content))
    result = response.full_text_annotation
    blocks: list[dict] = []
    for page in result.pages:
        for block in page.blocks:
            blocks.append({"text": normalize_text(" ".join(getattr(word, "text", "") for para in block.paragraphs for word in para.words)), "confidence": block.confidence})
    return blocks
