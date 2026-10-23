
class DocumentExtractionRequest:
    def __init__(self, document_path: str, document_type: str):
        self.document_path = document_path
        self.document_type = document_type

class DocumentExtractionResponse:
    def __init__(self, extracted_fields: dict, confidence_scores: dict):
        self.extracted_fields = extracted_fields
        self.confidence_scores = confidence_scores

class NormalizedDocument:
    def __init__(self, normalized_data: dict, schema_version: str = "1.0"):
        self.normalized_data = normalized_data
        self.schema_version = schema_version
