import os
import json
from typing import Dict, Any
from google.cloud import language_v1
from document_models import TextExtractionResponse

def extract_fields(text_response: TextExtractionResponse) -> Dict[str, Any]:
    """Extract structured fields from OCR-normalized document text using Google Cloud Natural Language."""
    client = language_v1.LanguageServiceClient()
    
    text = text_response.full_text
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    entities_response = client.analyze_entities(request={"document": document})
    
    fields = {}
    for entity in entities_response.entities:
        fields[entity.name] = {
            "type": language_v1.Entity.Type(entity.type_).name,
            "salience": entity.salience,
            "metadata": entity.metadata
        }
    
    return {
        "fields": fields,
        "provider": "google_cloud_natural_language",
        "model": "v1"
    }