# SAME-SCENARIO extract_tables.py

import os
import json
from google.cloud import documentai_v1 as documentai

PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
DOCUMENT_AI_URI = os.getenv(
    "GOOGLE_DOCUMENTAI_URI", f"projects/{PROJECT_ID}/locations/{LOCATION}/processors"
)


class GoogleDocumentAI:
    """Local wrapper for Google Document AI OCR and table extraction."""

    def __init__(self, creds_path: str):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
        self.client = documentai.DocumentProcessorServiceClient()

    def process_image(self, image_path: str):
        """Run OCR on an image and return parsed tables."""
        name = f"{DOCUMENT_AI_URI}/processor:process"
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        response = self.client.process_document(
            request={
                "name": name,
                "raw_document": {"content": image_bytes, "mime_type": "image/jpeg"},
            }
        )
        tables = []
        for page in response.document.pages:
            for entity in page.entities:
                # Entity.type == 'TABLE' for tables in Document AI
                if entity.type == "TABLE":
                    table = {
                        "rows": len(entity.properties["rows"].list_value.values),
                        "cols": len(entity.properties["cols"].list_value.values),
                        "cells": [],
                    }
                    tables.append(table)
        return tables


if __name__ == "__main__":
    # Sample usage – replace with real credentials and image path
    creds = "path/to/google-credentials.json"
    gda = GoogleDocumentAI(creds)
    tables = gda.process_image("sample_invoice.jpg")
    print(f"Found {len(tables)} tables")
    # Uncomment to see details of the first table
    # print(json.dumps(tables[0], indent=2))
