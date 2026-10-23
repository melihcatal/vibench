from typing import Dict, Any, List


class DocumentExtractionRequest:
    def __init__(
        self,
        project_id: str,
        location: str,
        processor_id: str,
        file_content: bytes,
        mime_type: str,
    ):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.file_content = file_content
        self.mime_type = mime_type


class DocumentExtractionResponse:
    def __init__(self, extracted_data: Any):
        self.extracted_data = extracted_data


class TranslationRequest:
    def __init__(self, text: str, target_language: str, source_language: str = None):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language


class TranslationResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text


class SafetyCheckRequest:
    def __init__(self, text: str):
        self.text = text


class SafetyCheckResponse:
    def __init__(self, unsafe_categories: List[str], scores: Dict[str, float]):
        self.unsafe_categories = unsafe_categories
        self.scores = scores


class FieldExtractionRequest:
    def __init__(
        self,
        project_id: str,
        location: str,
        processor_id: str,
        file_content: bytes,
        mime_type: str,
    ):
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.file_content = file_content
        self.mime_type = mime_type


class FieldExtractionResponse:
    def __init__(self, fields: Dict[str, Any]):
        self.fields = fields


class EmbeddingRequest:
    def __init__(self, text_segments: List[str]):
        self.text_segments = text_segments


class EmbeddingResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings
