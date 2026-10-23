from dataclasses import dataclass

@dataclass
class TranscriptChunk:
    text: str
    start_time: float
    end_time: float
    is_final: bool

@dataclass
class TranslationResult:
    text: str
    source_language: str
    target_language: str

@dataclass
class SafetyResult:
    categories: dict # e.g., {'Hate': 0, 'SelfHarm': 0, 'Sexual': 0, 'Violence': 0}
    is_safe: bool

@dataclass
class SummaryResult:
    summary_text: str
    source_text_length: int
    summary_text_length: int

@dataclass
class EmbeddingResult:
    embedding_vector: list[float]
    text: str
