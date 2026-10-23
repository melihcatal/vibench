import os
from google.cloud import documentai_v1 as documentai

# Google Document AI requires GOOGLE_APPLICATION_CREDENTIALS env var
client = documentai.DocumentProcessorServiceClient()

def extract_text_from_image(image_path: str) -> str:
    # Encode image bytes
    with open(image_path, 'rb') as img:
        content = img.read()
    # Build Document request
    raw = documentai.Document(content=content, mime_type='image/jpeg')
    # Call processor (set PROCESSOR_ID env variable)
    name = os.getenv('DOCUMENTAI_PROCESSOR_ID')
    resp = client.process_document(name=name, raw_document=raw)
    # Return plain text
    return resp.document.text
