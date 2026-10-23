from dataclasses import dataclass
from typing import List

@dataclass
class EmbeddedDocument:
    """
    Represents a document with its corresponding embedding vector.
    """
    text: str
    embedding: List[float]

@dataclass
class SearchResult:
    """
    Represents a search result, including the document and its similarity score.
    """
    document: EmbeddedDocument
    score: float
