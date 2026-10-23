import json
from typing import Dict, Any, List

# HELPER: document_models.py

# Shared models for OCR/layout extraction and downstream steps


class OCRRequest:
    """Request model for OCR extraction.

    Attributes:
        image_bytes (bytes): Binary content of the scanned document.
        language (str, optional): Language code for OCR (e.g., 'en').
    """

    def __init__(self, image_bytes: bytes, language: str = "en"):
        self.image_bytes = image_bytes
        self.language = language

    def to_dict(self) -> Dict[str, Any]:
        return {"image_bytes": self.image_bytes, "language": self.language}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(image_bytes=data["image_bytes"], language=data.get("language", "en"))


class OCRResponse:
    """Response model for OCR extraction.

    Attributes:
        text (str): Extracted plain text.
        layout (Dict): Hierarchical layout information (blocks, lines, tables).
        tables (List[Dict]): List of extracted tables.
        kvs (Dict): Extracted key‑value pairs.
    """

    def __init__(
        self,
        text: str,
        layout: Dict[str, Any],
        tables: List[Dict[str, Any]],
        kvs: Dict[str, str],
    ):
        self.text = text
        self.layout = layout
        self.tables = tables
        self.kvs = kvs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "layout": self.layout,
            "tables": self.tables,
            "key_values": self.kvs,
        }


class TranslationRequest:
    """Request model for text translation.

    Attributes:
        source_text (str): Text to translate.
        target_language (str): Target language code.
    """

    def __init__(self, source_text: str, target_language: str):
        self.source_text = source_text
        self.target_language = target_language

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_text": self.source_text,
            "target_language": self.target_language,
        }


class TranslationResponse:
    """Response model for text translation.

    Attributes:
        translated_text (str): Translated text.
    """

    def __init__(self, translated_text: str):
        self.translated_text = translated_text

    def to_dict(self) -> Dict[str, Any]:
        return {"translated_text": self.translated_text}


class ContentSafetyRequest:
    """Request model for content safety checks.

    Attributes:
        text (str): Text to evaluate.
        category (str, optional): Specific safety category (e.g., 'hate', 'sexual', 'self_harm').
    """

    def __init__(self, text: str, category: str = None):
        self.text = text
        self.category = category

    def to_dict(self) -> Dict[str, Any]:
        d = {"text": self.text}
        if self.category:
            d["category"] = self.category
        return d


class ContentSafetyResponse:
    """Response model for content safety checks.

    Attributes:
        is_safe (bool): Whether the text is considered safe.
        flags (List[str]): List of detected unsafe categories or reasons.
    """

    def __init__(self, is_safe: bool, flags: List[str] = None):
        self.is_safe = is_safe
        self.flags = flags or []

    def to_dict(self) -> Dict[str, Any]:
        return {"is_safe": self.is_safe, "flags": self.flags}


class FieldExtractionRequest:
    """Request model for structured field extraction from normalized OCR text.

    Attributes:
        raw_text (str): OCR‑normalized plain text of the document.
        schema (Dict[str, str]): Mapping of field names to extraction patterns/keys.
    """

    def __init__(self, raw_text: str, schema: Dict[str, str]):
        self.raw_text = raw_text
        self.schema = schema

    def to_dict(self) -> Dict[str, Any]:
        return {"raw_text": self.raw_text, "schema": self.schema}


class FieldExtractionResponse:
    """Response model for structured field extraction.

    Attributes:
        fields (Dict[str, str]): Extracted field names mapped to their values.
    """

    def __init__(self, fields: Dict[str, str]):
        self.fields = fields

    def to_dict(self) -> Dict[str, Any]:
        return {"fields": self.fields}


class EmbeddingRequest:
    """Request model for generating embeddings from document sections.

    Attributes:
        text (str): Document section text to embed.
        model_id (str, optional): Identifier for the embedding model.
    """

    def __init__(self, text: str, model_id: str = "default"):
        self.text = text
        self.model_id = model_id

    def to_dict(self) -> Dict[str, Any]:
        d = {"text": self.text}
        if self.model_id != "default":
            d["model_id"] = self.model_id
        return d


class EmbeddingResponse:
    """Response model for embeddings.

    Attributes:
        vector (List[float]): The embedding vector.
        model_id (str): Identifier of the model used.
    """

    def __init__(self, vector: List[float], model_id: str = "default"):
        self.vector = vector
        self.model_id = model_id

    def to_dict(self) -> Dict[str, Any]:
        return {"vector": self.vector, "model_id": self.model_id}


# Example helper to normalise raw OCR output into a unified OCRResponse


def normalize_ocr_output(textract_response) -> OCRResponse:
    # This function assumes the response from Amazon Textract's analyze_document API
    text = "\n".join(
        block["Text"]
        for block in textract_response.get("Blocks", [])
        if block["BlockType"] == "LINE"
    )
    layout = {"blocks": [], "lines": [], "tables": []}
    for block in textract_response.get("Blocks", []):
        if block["BlockType"] == "LINE":
            layout["lines"].append(block["Text"])
        elif block["BlockType"] == "TABLE":
            layout["tables"].append(block)
        else:
            layout["blocks"].append(block)
    # Simple key‑value extraction using relationships (omitted for brevity)
    kvs = {}
    for block in textract_response.get("Blocks", []):
        if block.get("BlockType") == "KEY_VALUE_SET":
            key, value = "", ""
            for rel in block.get("Relationships", []):
                for id_info in rel.get("Ids", []):
                    # Determine key vs value by entity type
                    # (not fully implemented for brevity)
                    pass
            kvs[key] = value
    return OCRResponse(text=text, layout=layout, tables=[], kvs=kvs)


# End of file
