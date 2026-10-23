import re
from typing import Dict, List, Any
from document_models import DocumentResponse, ExtractedDocument

class DocumentFieldExtraction:
    @staticmethod
    def extract_metadata(text: str) -> Dict[str, str]:
        # Simple regex patterns for common fields (extend as needed)
        patterns = {
            'date': r'(\\d{1,2}[/-]\\d{1,2}[/-]\\d{2,4})',
            'invoice_number': r'INV[- ]?(\\d+)',
            'total_amount': r'(?:Total|Amount)[ :\\$]?(\\d+(?:[.,]\\d+)?)'
        }
        metadata: Dict[str, str] = {}
        for key, pat in patterns.items():
            match = re.search(pat, text)
            if match:
                metadata[key] = match.group(1).strip()
        return metadata

    @staticmethod
    def build_structured_output(response: DocumentResponse) -> ExtractedDocument:
        # Assume response is from Google Document AI normalized output
        # Pull plain text, layout, tables, and key-values
        raw = response.raw  # type: ignore
        # Example: raw may have fields like 'document.text', 'document.entities', etc.
        # Here we demonstrate extraction using simple heuristics on the plain text
        text = raw.get('text', '')
        metadata = DocumentFieldExtraction.extract_metadata(text)
        # Treat all entities as structured fields (in real use, map entity types)
        fields: Dict[str, Any] = {}
        for ent in raw.get('layout', []):
            fields[ent.get('type', 'other')] = ent.get('text', '')
        return ExtractedDocument(
            text=text,
            layout=raw.get('layout', []),
            tables=raw.get('tables', []),
            kv=metadata  # simple key-values
        )
