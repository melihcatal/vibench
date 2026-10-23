import os
from typing import Dict, Any
from google.cloud import language_v1
from document_models import OCRTextResponse

def extract_fields(text_response: OCRTextResponse) -> Dict[str, Any]:
    """Extract structured fields from OCR-normalized document text using Google Natural Language API."""
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text_response.text, 
        type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    response = client.analyze_entities(request={"document": document})
    
    fields = {}
    for entity in response.entities:
        fields[entity.name] = {
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience,
            "metadata": entity.metadata
        }
    
    return fields