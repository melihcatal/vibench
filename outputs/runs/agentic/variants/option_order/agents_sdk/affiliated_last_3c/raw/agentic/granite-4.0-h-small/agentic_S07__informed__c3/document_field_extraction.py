# Extract structured fields from OCR-normalized document text
import re
from document_models import OCRResponse, LayoutElement

class FieldExtractor:
    """Utility that converts plain text and layout into structured fields."""
    def __init__(self, layout: LayoutElement, text: str):
        self.layout = layout
        self.text = text

    def extract_fields(self) -> dict:
        """Simple heuristic: look for patterns like \"Date:\", \"Amount:\", etc."""
        fields = {}
        # Example patterns; extend as needed
        patterns = {
            'Date': r\"Date[:\s]+([\d/-]+)\",
            'Amount': r\"Amount[:\s]+([$€\\d,.]+)\",
            'Name': r\"Name[:\s]+([A-Za-z ]+)\",
        }
        for label, pat in patterns.items():
            m = re.search(pat, self.text)
            if m:
                fields[label] = m.group(1).strip()
        return fields

    @classmethod
    def from_response(cls, resp: OCRResponse) -> 'FieldExtractor':
        return cls(resp['layout'], resp['text'])
