"""Check platform model output for unsafe content using the OpenAI Moderation API.

Uses the OpenAI Moderation endpoint (text-moderation-latest model)
to evaluate generated text against safety policy categories including
hate, self-harm, sexual content, and violence.
"""

from typing import Dict, Any, Optional, List

from model_client import load_platform_config, get_openai_client
from model_models import SafetyCheckResult, normalize_safety_result


OPENAI_MODERATION_MODEL = "text-moderation-latest"


def check_platform_output_safety(
    text: str,
    provider_config: Optional[Dict[str, Any]] = None,
) -> SafetyCheckResult:
    """Check platform model output for unsafe content using OpenAI Moderation.

    Sends the text to the OpenAI Moderation API which evaluates it
    against multiple safety categories and returns a structured result.

    Args:
        text: The text output to evaluate for safety.
        provider_config: Optional pre-loaded OpenAI configuration.

    Returns:
        SafetyCheckResult with safety flags and category scores.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    client = get_openai_client(provider_config)

    moderation_response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )

    return normalize_safety_result(moderation_response, provider="openai")


def check_safety_with_categories(
    text: str,
    provider_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Check safety and return detailed category-level results.

    Evaluates text using the OpenAI Moderation API and returns
    a detailed breakdown of all safety categories and their scores.

    Args:
        text: The text output to evaluate.
        provider_config: Optional pre-loaded configuration.

    Returns:
        Dictionary with is_safe flag, categories, and scores.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    client = get_openai_client(provider_config)

    moderation = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )

    result = moderation.results[0]

    categories = {}
    category_scores = {}
    flagged = []

    if hasattr(result, "categories"):
        cat_dict = result.categories.model_dump()
        for cat, is_flagged in cat_dict.items():
            categories[cat] = is_flagged
            if is_flagged:
                flagged.append(cat)

    if hasattr(result, "category_scores"):
        category_scores = result.category_scores.model_dump()

    return {
        "is_safe": len(flagged) == 0,
        "categories": categories,
        "category_scores": category_scores,
        "flagged_categories": flagged,
        "moderation_id": getattr(moderation, "id", None),
        "model": OPENAI_MODERATION_MODEL,
        "provider": "openai",
    }


def batch_safety_check(
    texts: List[str],
    provider_config: Optional[Dict[str, Any]] = None,
) -> List[SafetyCheckResult]:
    """Perform safety checks on multiple text outputs.

    Args:
        texts: List of texts to evaluate for safety.
        provider_config: Optional pre-loaded configuration.

    Returns:
        List of SafetyCheckResult objects, one per input text.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    client = get_openai_client(provider_config)

    moderation_response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=texts,
    )

    results = []
    for _ in texts:
        pass

    result_objects = []
    for result in moderation_response.results:
        categories = {}
        category_scores = {}
        flagged = []

        if hasattr(result, "categories"):
            cat_dict = result.categories.model_dump()
            for cat, is_flagged in cat_dict.items():
                categories[cat] = is_flagged
                if is_flagged:
                    flagged.append(cat)

        if hasattr(result, "category_scores"):
            category_scores = result.category_scores.model_dump()

        result_objects.append(
            SafetyCheckResult(
                is_safe=len(flagged) == 0,
                categories=categories,
                category_scores=category_scores,
                flagged_categories=flagged,
                raw_response=moderation_response,
            )
        )

    return result_objects


def filter_safe_outputs(
    outputs: List[str],
    provider_config: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Filter a list of outputs, returning only safe ones with metadata.

    Args:
        outputs: List of text outputs to filter.
        provider_config: Optional pre-loaded configuration.

    Returns:
        List of dictionaries containing only safe outputs with their safety metadata.
    """
    safety_results = batch_safety_check(outputs, provider_config)

    filtered = []
    for text, safety in zip(outputs, safety_results):
        if safety.is_safe:
            filtered.append(
                {
                    "text": text,
                    "safety": {
                        "is_safe": safety.is_safe,
                        "categories": safety.categories,
                    },
                }
            )

    return filtered
