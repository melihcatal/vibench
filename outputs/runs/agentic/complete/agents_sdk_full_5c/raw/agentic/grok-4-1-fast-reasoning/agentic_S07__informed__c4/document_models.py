from typing import Any, Dict, List, Union

OcrText = str
LayoutElement = Dict[str, Any]
TableStructure = List[List[str]]
KeyValuePair = Dict[str, str]
EmbeddingVector = List[float]

def normalize_extracted_text(text: str) -> str:
    """Normalize OCR extracted text."""
    return ' '.join(text.split())
