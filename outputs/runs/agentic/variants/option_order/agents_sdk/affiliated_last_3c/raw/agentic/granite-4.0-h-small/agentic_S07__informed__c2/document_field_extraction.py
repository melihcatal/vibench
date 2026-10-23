import json
from document_models import DocumentKeyValueResponse, KeyValuePair

class DocumentFieldExtractor:
    def __init__(self):
        pass

    @staticmethod
    def select_fields(response: DocumentKeyValueResponse, schema: Dict[str, str]) -> Dict[str, str]:
        """
        Given a key‑value OCR response and a schema dict that maps desired field names
        to OCR key strings, extract the corresponding values.
        """
        extracted = {}
        for kv in response["pairs"]:
            key_text = kv["key"]["content"].lower()
            desired_key = next(iter(schema), None)
            if desired_key and key_text == schema[desired_key].lower():
                extracted[desired_key] = kv["value"]["content"]
        return extracted

    @staticmethod
    def parse_response(raw_json: str) -> DocumentKeyValueResponse:
        return json.loads(raw_json)

if __name__ == "__main__":
    # Example usage
    schema = {
        "invoice_number": "Invoice No.",
        "total_amount": "Total"
    }
    from extract_key_values import ExtractKeyValues
    extractor = ExtractKeyValues()
    doc = extractor.extract("sample_invoice.jpg")
    data = DocumentFieldExtractor.parse_response(doc)
    fields = DocumentFieldExtractor.select_fields(data, schema)
    print(fields)
