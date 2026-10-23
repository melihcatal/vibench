import os
from google.cloud import documentai_v1 as documentai

# Google Document AI requires GOOGLE_APPLICATION_CREDENTIALS env var
client = documentai.DocumentProcessorServiceClient()

def extract_layout_from_image(image_path: str):
    with open(image_path, 'rb') as img:
        content = img.read()
    raw = documentai.Document(content=content, mime_type='image/jpeg')
    name = os.getenv('DOCUMENTAI_PROCESSOR_ID')
    resp = client.process_document(name=name, raw_document=raw)
    # Normalize layout fields
    doc = resp.document
    blocks = [b for b in doc.blocks]
    lines = [l for l in doc.pages[0].layout.lines]
    tokens = [t for t in doc.pages[0].layout.tokens]
    return {
        'blocks': blocks,
        'lines': lines,
        'tokens': tokens
    }
