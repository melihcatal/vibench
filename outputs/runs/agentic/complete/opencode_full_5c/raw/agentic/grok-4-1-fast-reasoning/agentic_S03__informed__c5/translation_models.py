from typing import TypedDict, List, Optional, Union


class TranslationResult(TypedDict):
    translated_text: str
    detected_source_language: Optional[str]


def normalize_input(text_input: Union[str, List[str]]) -> Union[str, List[str]]:
    if isinstance(text_input, str):
        normalized = text_input.strip()
        if not normalized:
            raise ValueError("Input text cannot be empty")
        return normalized
    else:
        normalized_texts = [normalize_input(t) for t in text_input]
        if not normalized_texts:
            raise ValueError("Input texts list cannot be empty")
        return normalized_texts
