# SAME-SCENARIO extract_key_values.py

import os
import json
from google.cloud import documentai_v1 as documentai

PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
DOCUMENT_AI_URI = os.getenv(
    "GOOGLE_DOCUMENTAI_URI", f"projects/{PROJECT_ID}/locations/{LOCATION}/processors"
)


class GoogleDocumentAI:
    """Local wrapper for Google Document AI OCR and key-value pair extraction."""

    def __init__(self, creds_path: str):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
        self.client = documentai.DocumentProcessorServiceClient()

    def process_and_extract_kv(self, image_path: str):
        """Process an image and return extracted key-value pairs and entities."""
        name = f"{DOCUMENT_AI_URI}/processor:process"
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        response = self.client.process_document(
            request={
                "name": name,
                "raw_document": {"content": image_bytes, "mime_type": "image/jpeg"},
            }
        )
        kv_pairs = []
        entities = []
        # Document AI returns entities like KEY, VALUE, LABEL etc.
        for entity in response.document.entities:
            desc = {
                "id": entity.name,
                "type": entity.type,
                "text": entity.mention_text,
                "confidence": entity.confidence,
            }
            if entity.type == "KEY":
                kv_pairs.append({"key": desc})
            elif entity.type == "VALUE":
                kv_pairs[-1]["value"] = desc
            else:
                entities.append(desc)
        return {"key_values": kv_pairs, "other_entities": entities}


if __name__ == "__main__":
    creds = "path/to/google-credentials.json"
    gda = GoogleDocumentAI(creds)
    result = gda.process_and_extract_kv("sample_form.jpg")
    print("Key-Value pairs:", result["key_values"][:5])
    print("Other entities:", result["other_entities"][:5])
