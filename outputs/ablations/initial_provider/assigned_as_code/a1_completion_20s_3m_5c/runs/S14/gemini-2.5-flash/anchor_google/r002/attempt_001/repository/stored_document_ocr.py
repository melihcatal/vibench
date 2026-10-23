from typing import Optional

from google.cloud import vision
from storage_client import get_bucket_name
from storage_models import StoredDocumentOcrPayload, StorageConfig

def stored_document_ocr(payload: StoredDocumentOcrPayload, config: Optional[StorageConfig] = None) -> dict:
    client = vision.ImageAnnotatorClient()
    bucket_name = get_bucket_name(config)
    image = vision.Image({"source": {"image_uri": f"gs://{bucket_name}/{payload.object_name}"}})
    
    response = client.document_text_detection(image=image, image_context=vision.ImageContext(language_hints=payload.language_hints))

    full_text = response.full_text_annotation.text
    pages_text = []
    for page in response.full_text_annotation.pages:
        page_text = []
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    page_text.append(word_text)
        pages_text.append(' '.join(page_text))

    return {"full_text": full_text, "pages_text": pages_text}
