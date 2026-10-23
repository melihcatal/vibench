"""
Check corpus text before embedding.

Provider: OpenAI Moderation API (https://api.openai.com)
Model: omni-moderation-latest
"""

from typing import List, Optional, Dict, Any

from openai import OpenAI

from embeddings_client import get_openai_client


SAFETY_FLAGGED = "flagged"
SAFETY_SAFE = "safe"


class SafetyResult:
    """
    Result of a safety check on a text item.

    Attributes:
        text: The original text
        is_safe: Whether the text passed safety checks
        categories: Dict of safety category flags
        category_scores: Dict of category confidence scores
    """

    def __init__(
        self,
        text: str,
        is_safe: bool = True,
        categories: Optional[Dict[str, bool]] = None,
        category_scores: Optional[Dict[str, float]] = None,
    ):
        self.text = text
        self.is_safe = is_safe
        self.categories = categories or {}
        self.category_scores = category_scores or {}

    @property
    def status(self) -> str:
        return SAFETY_SAFE if self.is_safe else SAFETY_FLAGGED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text_preview": self.text[:100] + ("..." if len(self.text) > 100 else ""),
            "status": self.status,
            "is_safe": self.is_safe,
            "flagged_categories": [
                cat for cat, flagged in self.categories.items() if flagged
            ],
        }


class CorpusSafetyReport:
    """
    Aggregate safety report for a corpus of texts.

    Attributes:
        total_items: Total texts checked
        safe_items: Number of texts that passed safety checks
        flagged_items: Number of texts flagged by moderation
        results: List of individual SafetyResult objects
    """

    def __init__(self):
        self.total_items = 0
        self.safe_items = 0
        self.flagged_items = 0
        self.results: List[SafetyResult] = []

    @property
    def safety_rate(self) -> float:
        if self.total_items == 0:
            return 0.0
        return self.safe_items / self.total_items

    def add_result(self, result: SafetyResult) -> None:
        self.results.append(result)
        self.total_items += 1
        if result.is_safe:
            self.safe_items += 1
        else:
            self.flagged_items += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_items": self.total_items,
            "safe_items": self.safe_items,
            "flagged_items": self.flagged_items,
            "safety_rate": round(self.safety_rate, 4),
            "flagged_texts": [
                r.to_dict() for r in self.results if not r.is_safe
            ],
        }


def check_text_safety(
    text: str,
    api_key: Optional[str] = None,
    model: str = "omni-moderation-latest",
) -> SafetyResult:
    """
    Check a single text for safety violations using OpenAI's Moderation API.

    Uses the omni-moderation-latest model from OpenAI to detect harmful,
    illegal, or policy-violating content.

    Args:
        text: Text to check for safety
        api_key: OpenAI API key
        model: OpenAI moderation model (default: omni-moderation-latest)

    Returns:
        SafetyResult with safety status and category details

    Raises:
        ValueError: If text is empty
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    client = get_openai_client(api_key=api_key)

    response = client.moderations.create(
        model=model,
        input=text,
    )

    result_data = response.results[0]
    categories = {}
    category_scores = {}

    for cat_name in result_data.categories.model_dump():
        flagged = getattr(result_data.categories, cat_name, False)
        score = getattr(result_data.category_scores, cat_name, 0.0)
        categories[cat_name] = flagged
        category_scores[cat_name] = score

    return SafetyResult(
        text=text,
        is_safe=not result_data.flagged,
        categories=categories,
        category_scores=category_scores,
    )


def check_corpus_safety(
    texts: List[str],
    api_key: Optional[str] = None,
    model: str = "omni-moderation-latest",
    batch_size: int = 32,
) -> CorpusSafetyReport:
    """
    Check an entire corpus of texts for safety before embedding.

    Processes texts in batches using OpenAI's Moderation API with the
    omni-moderation-latest model.

    Args:
        texts: List of texts to check
        api_key: OpenAI API key
        model: OpenAI moderation model (default: omni-moderation-latest)
        batch_size: Texts per API call

    Returns:
        CorpusSafetyReport with aggregate safety statistics
    """
    report = CorpusSafetyReport()

    if not texts:
        return report

    client = get_openai_client(api_key=api_key)

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        try:
            response = client.moderations.create(
                model=model,
                input=batch,
            )

            for text, result_data in zip(batch, response.results):
                categories = {}
                category_scores = {}

                for cat_name in result_data.categories.model_dump():
                    flagged = getattr(result_data.categories, cat_name, False)
                    score = getattr(result_data.category_scores, cat_name, 0.0)
                    categories[cat_name] = flagged
                    category_scores[cat_name] = score

                safety_result = SafetyResult(
                    text=text,
                    is_safe=not result_data.flagged,
                    categories=categories,
                    category_scores=category_scores,
                )
                report.add_result(safety_result)

        except Exception:
            for text in batch:
                report.add_result(
                    SafetyResult(text=text, is_safe=False)
                )

    return report


def filter_safe_texts(
    texts: List[str],
    api_key: Optional[str] = None,
    model: str = "omni-moderation-latest",
) -> List[str]:
    """
    Filter a corpus to only include texts that pass safety checks.

    Args:
        texts: List of texts to filter
        api_key: OpenAI API key
        model: OpenAI moderation model (default: omni-moderation-latest)

    Returns:
        List of texts that passed OpenAI moderation checks
    """
    report = check_corpus_safety(texts, api_key=api_key, model=model)
    return [r.text for r in report.results if r.is_safe]


if __name__ == "__main__":
    import json

    sample_texts = [
        "This is a perfectly safe document about machine learning.",
        "Another benign text about natural language processing.",
    ]
    report = check_corpus_safety(sample_texts)
    print(json.dumps(report.to_dict(), indent=2))
