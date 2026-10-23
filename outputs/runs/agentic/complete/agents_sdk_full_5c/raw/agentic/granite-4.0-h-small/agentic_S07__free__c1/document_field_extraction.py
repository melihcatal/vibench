import os
import re
from typing import List, Tuple, Dict
from dotenv import load_dotenv
from document_models import FieldExtractionRequest, FieldExtractionResponse, Field, FieldType

load_dotenv()
FIELD_API_URL = os.getenv('FIELD_API_URL', 'https://api.formfieldextractor.com/v1/fields')
FIELD_API_KEY = os.getenv('FIELD_API_KEY')

async def extract_fields(text: str, schema: Dict[str, FieldType]) -> FieldExtractionResponse:
    """Extract structured fields from OCR-normalized document text using a hosted form parser."""
    payload = {
        "text": text,
        "schema": schema
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            FIELD_API_URL,
            json=payload,
            headers={"Authorization": f"Bearer {FIELD_API_KEY}"},
        )
        resp.raise_for_status()
        data = resp.json()
        fields = [Field(name=k, value=v, type_=schema[k]) for k, v in data['extracted'].items()]
        return FieldExtractionResponse(fields=fields)
