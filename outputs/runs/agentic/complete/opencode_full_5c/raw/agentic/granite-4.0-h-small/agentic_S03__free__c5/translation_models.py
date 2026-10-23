from typing import TypedDict, Literal, Any

class GeneralTextRequest(TypedDict):
    source_text: str
    source_lang: str
    target_lang: str

class GeneralMarkupRequest(TypedDict):
    source_markup: str
    source_lang: str
    target_lang: str

class GeneralTextResponse(TypedDict):
    translated_text: str

class GeneralMarkupResponse(TypedDict):
    translated_markup: str

class QualityIssue(TypedDict):
    type: Literal["unsafe_content", "fluent", "consistent"]
    description: str
    severity: Literal["error", "warning"]

class TranslationScore(TypedDict):
    quality_issue: QualityIssue | None
    raw_score: float
    normalized_score: float

# Normalization utilities
ScoreNormalization = Literal["zscore", "percentile", "raw"]

def normalize_score(raw: float, method: ScoreNormalization = "raw") -> float:
    """Normalize a raw quality score.

    Args:
        raw: Raw numeric score from provider.
        method: Normalization approach to apply.

    Returns:
        Normalized score in 0-1 range.
    """
    if method == "zscore":
        # Placeholder: apply z-score transformation
n        return (raw - 0.5) / 0.2  # example scaling
    if method == "percentile":
        # Placeholder: convert to percentile
        return raw / 100.0
    return raw  # raw mode returns unchanged
