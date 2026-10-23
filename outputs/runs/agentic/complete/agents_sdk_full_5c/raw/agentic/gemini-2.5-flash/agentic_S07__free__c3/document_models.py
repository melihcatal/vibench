from typing import List, Dict, Any
from google.cloud import documentai_v1 as documentai

class DocumentTextSegment:
    """Represents a segment of text within a document, potentially with bounding box info."""
    def __init__(self, text: str, page_number: int = None, bounding_box: List[Dict[str, float]] = None):
        self.text = text
        self.page_number = page_number
        self.bounding_box = bounding_box  # List of dicts, e.g., [{'x': 0.1, 'y': 0.2}, ...]

class KeyValuePair:
    """Represents an extracted key-value pair."""
    def __init__(self, key: str, value: str, key_bounding_box: List[Dict[str, float]] = None, value_bounding_box: List[Dict[str, float]] = None):
        self.key = key
        self.value = value
        self.key_bounding_box = key_bounding_box
        self.value_bounding_box = value_bounding_box

class ProcessedDocument:
    """A normalized representation of a document after OCR and layout extraction."""
    def __init__(self, full_text: str = "", text_segments: List[DocumentTextSegment] = None, tables: List[Dict[str, Any]] = None, key_value_pairs: List[KeyValuePair] = None):
        self.full_text = full_text
        self.text_segments = text_segments if text_segments is not None else []
        self.tables = tables if tables is not None else []
        self.key_value_pairs = key_value_pairs if key_value_pairs is not None else []

    @staticmethod
    def from_documentai_document(doc_ai_document: documentai.Document) -> 'ProcessedDocument':
        """Converts a Document AI Document object into a normalized ProcessedDocument."""
        full_text = doc_ai_document.text
        text_segments = []
        key_value_pairs = []

        for page in doc_ai_document.pages:
            for paragraph in page.paragraphs:
                text_segments.append(DocumentTextSegment(
                    text=doc_ai_document.text[paragraph.layout.text_anchor.start:paragraph.layout.text_anchor.end],
                    page_number=page.page_number,
                    # Bounding box conversion would be more complex, simplify for example
                    # bounding_box=[{'x': vertex.x, 'y': vertex.y} for vertex in paragraph.layout.bounding_poly.normalized_vertices]
                ))
        
        for entity in doc_ai_document.entities:
            if entity.type_ == "form_field": # or other relevant entity types
                key = doc_ai_document.text[entity.text_anchor.start:entity.text_anchor.end] if entity.text_anchor.start is not None else entity.mention_text
                value = doc_ai_document.text[entity.value_anchor.start:entity.value_anchor.end] if entity.value_anchor.start is not None else entity.normalized_value.text
                key_value_pairs.append(KeyValuePair(key=key, value=value))

        # Tables extraction would involve iterating through doc_ai_document.pages[i].tables
        # and constructing a structured representation.

        return ProcessedDocument(full_text=full_text, text_segments=text_segments, key_value_pairs=key_value_pairs)

# Example usage:
# from google.cloud import documentai_v1 as documentai
# mock_doc = documentai.Document(text="Hello world")
# processed_doc = ProcessedDocument.from_documentai_document(mock_doc)
# print(processed_doc.full_text)
