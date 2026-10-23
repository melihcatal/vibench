import os
from google.cloud import documentai_v1 as documentai

# Google Document AI requires GOOGLE_APPLICATION_CREDENTIALS env var
client = documentai.DocumentProcessorServiceClient()

def extract_key_values_from_image(image_path: str):
    with open(image_path, 'rb') as img:
        content = img.read()
    raw = documentai.Document(content=content, mime_type='image/jpeg')
    name = os.getenv('DOCUMENTAI_PROCESSOR_ID')
    resp = client.process_document(name=name, raw_document=raw)
    doc = resp.document
    # Simple heuristic: treat first line as key, second as value
    kv = {}
    lines = [p.text for p in doc.pages[0].paragraphs]
    for i in range(0, len(lines), 2):
        if i+1 < len(lines):
            kv[lines[i].strip()] = lines[i+1].strip()
    return kv
