import os
from typing import Dict, List
import json

# ---------- Provider credentials ----------
AZURE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
MINDEE_API_KEY = os.getenv("MINDEE_API_KEY")


# ---------- Structured field extraction (North American driver's license example) ----------
class FieldExtractor:
    """Extract structured key‑value pairs from OCR‑normalized text or JSON payloads."""

    def __init__(self, provider: str):
        self.provider = provider.lower()
        # Simple mapping from provider to extraction helper
        if self.provider == "azure":
            self.extract = self._extract_azure
        elif self.provider == "google":
            self.extract = self._extract_google
        elif self.provider == "mindee":
            self.extract = self._extract_mindee
        else:
            raise ValueError(f"Unsupported provider for field extraction: {provider}")

    # ---------- Azure Document Intelligence ----------
    def _extract_azure(self, document: Dict[str, Any]) -> Dict[str, str]:
        """
        Use Azure Document Intelligence prebuilt model (e.g., document_type=IDENTIFICATION).
        Assumes `document` contains a `readResults` list with line items.
        """
        fields: Dict[str, str] = {}
        # Very naive rule‑based extraction for demonstration
        for result in document.get("readResults", []):
            for line in result.get("lines", []):
                text = line["text"].lower()
                if "driver" in text:
                    continue  # skip noisy lines
                if text.startswith("name"):
                    # take the next token as value placeholder (real pipeline would parse)
                    continue
                # Placeholder: we split on colon
                if ":" in line["text"]:
                    key, value = line["text"].split(":", 1)
                    fields[key.strip()] = value.strip()
        return fields

    # ---------- Google Document AI ----------
    def _extract_google(self, document: Dict[str, Any]) -> Dict[str, str]:
        fields: Dict[str, str] = {}
        # Google returns entities; we filter for known key names
        for entity in document.get("entities", []):
            name = entity.get("displayName", "").lower()
            value_text = entity.get("text", "")
            if name and value_text:
                fields[name] = value_text
        return fields

    # ---------- Mindee Form OCR ----------
    def _extract_mindee(self, document: Dict[str, Any]) -> Dict[str, str]:
        """
        Mindee form OCR already returns a `fields` list with key/value pairs.
        """
        return {f["key"]: f["value"] for f in document.get("fields", [])}

    # ---------- Public API ----------
    def run_extraction(self, raw_response: Dict[str, Any]) -> Dict[str, str]:
        """Run the appropriate extractor and return a dict of extracted fields."""
        return self.extract(raw_response)


# Example usage (run as script)
if __name__ == "__main__":
    # Simulated raw JSON from Azure Document Intelligence
    sample_azure = {
        "readResults": [
            {
                "lines": [
                    {"text": "NAME: John Doe"},
                    {"text": "DOB: 01/01/1980"},
                    {"text": "ADDRESS: 123 Main St"},
                ]
            }
        ]
    }
    extractor = FieldExtractor(provider="azure")
    fields = extractor.run_extraction(sample_azure)
    print("Extracted fields:", json.dumps(fields, indent=2))
