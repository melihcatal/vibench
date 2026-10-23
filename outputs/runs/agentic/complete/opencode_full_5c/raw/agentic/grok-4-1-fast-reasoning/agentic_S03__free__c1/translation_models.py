from typing import List, Dict, TypedDict


class SingleTranslation(TypedDict):
    text: str
    source_lang: str
    target_lang: str


class BatchTranslation(TypedDict):
    texts: List[str]
    source_lang: str
    target_lang: str


class QualitySummaryRequest(TypedDict):
    original: str
    translated: str
    source_lang: str
    target_lang: str


Embeddings = List[List[float]]
