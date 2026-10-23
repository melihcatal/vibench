import os
from typing import List, Dict, Any, Optional
from document_client import DocumentClient
from document_models import SafetyCheckResult


def check_text_safety(text: str, region: Optional[str] = None) -> SafetyCheckResult:
    client = DocumentClient(region_name=region)
    comprehend_client = client.get_comprehend_client()

    response = comprehend_client.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )

    result_list = response.get("ResultList", [])
    if not result_list:
        return SafetyCheckResult(
            text=text, is_safe=True, toxicity_score=0.0, categories={}
        )

    result = result_list[0]
    labels = result.get("Labels", [])

    toxicity_score = 0.0
    categories = {}

    for label in labels:
        category = label.get("Name", "")
        score = label.get("Score", 0.0)
        categories[category] = score
        toxicity_score = max(toxicity_score, score)

    is_safe = toxicity_score < 0.5

    return SafetyCheckResult(
        text=text, is_safe=is_safe, toxicity_score=toxicity_score, categories=categories
    )


def check_multiple_texts_safety(
    texts: List[str], region: Optional[str] = None
) -> List[SafetyCheckResult]:
    client = DocumentClient(region_name=region)
    comprehend_client = client.get_comprehend_client()

    text_segments = [{"Text": text, "Id": str(i)} for i, text in enumerate(texts)]

    response = comprehend_client.detect_toxic_content(
        TextSegments=text_segments, LanguageCode="en"
    )

    results = []
    result_map = {r.get("Id"): r for r in response.get("ResultList", [])}

    for i, text in enumerate(texts):
        result = result_map.get(str(i))
        if result:
            labels = result.get("Labels", [])
            toxicity_score = 0.0
            categories = {}

            for label in labels:
                category = label.get("Name", "")
                score = label.get("Score", 0.0)
                categories[category] = score
                toxicity_score = max(toxicity_score, score)

            is_safe = toxicity_score < 0.5

            results.append(
                SafetyCheckResult(
                    text=text,
                    is_safe=is_safe,
                    toxicity_score=toxicity_score,
                    categories=categories,
                )
            )
        else:
            results.append(
                SafetyCheckResult(
                    text=text, is_safe=True, toxicity_score=0.0, categories={}
                )
            )

    return results


def check_document_sections_safety(
    sections: Dict[str, str], region: Optional[str] = None
) -> Dict[str, SafetyCheckResult]:
    all_texts = list(sections.values())
    safety_results = check_multiple_texts_safety(all_texts, region)

    section_results = {}
    for (section_name, _), result in zip(sections.items(), safety_results):
        section_results[section_name] = result

    return section_results


def filter_unsafe_content(
    texts: List[str], threshold: float = 0.5, region: Optional[str] = None
) -> List[str]:
    safety_results = check_multiple_texts_safety(texts, region)

    safe_texts = []
    for result in safety_results:
        if result.toxicity_score < threshold:
            safe_texts.append(result.text)

    return safe_texts


def get_toxic_categories(text: str, region: Optional[str] = None) -> Dict[str, float]:
    result = check_text_safety(text, region)
    return result.categories


def is_text_safe_for_publication(text: str, region: Optional[str] = None) -> bool:
    result = check_text_safety(text, region)

    toxic_categories = [
        "HATE_SPEECH",
        "GRAPHIC",
        "HARASSMENT_OR_ABUSE",
        "SEXUAL",
        "VIOLENCE_OR_THREAT",
        "INSULT",
        "PROFANITY",
    ]

    for category in toxic_categories:
        if category in result.categories and result.categories[category] > 0.3:
            return False

    return result.toxicity_score < 0.4
