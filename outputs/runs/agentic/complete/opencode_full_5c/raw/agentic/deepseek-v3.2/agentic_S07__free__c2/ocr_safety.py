import os
from typing import List, Dict, Any, Optional
import requests


def check_ocr_text_safety(
    text: str, categories: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Check extracted document text for unsafe content using OpenAI Moderation API.

    Args:
        text: Text to check for safety
        categories: Optional list of specific categories to check

    Returns:
        Dictionary with safety analysis results
    """
    import openai

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))

    response = client.moderations.create(input=text, model="text-moderation-latest")

    result = response.results[0]

    safety_result = {
        "flagged": result.flagged,
        "categories": {},
        "category_scores": {},
        "overall_score": max(result.category_scores.values())
        if result.category_scores
        else 0.0,
    }

    for category, flagged in result.categories.model_dump().items():
        safety_result["categories"][category] = flagged

    for category, score in result.category_scores.model_dump().items():
        safety_result["category_scores"][category] = score

    if categories:
        filtered_categories = {}
        filtered_scores = {}
        for category in categories:
            if category in safety_result["categories"]:
                filtered_categories[category] = safety_result["categories"][category]
                filtered_scores[category] = safety_result["category_scores"][category]

        safety_result["filtered_categories"] = filtered_categories
        safety_result["filtered_scores"] = filtered_scores

    return safety_result


def check_batch_ocr_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """
    Check multiple OCR texts for safety using OpenAI Moderation API.

    Args:
        texts: List of texts to check

    Returns:
        List of safety analysis results for each text
    """
    import openai

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))

    response = client.moderations.create(input=texts, model="text-moderation-latest")

    results = []
    for result in response.results:
        safety_result = {
            "flagged": result.flagged,
            "categories": {},
            "category_scores": {},
            "overall_score": max(result.category_scores.values())
            if result.category_scores
            else 0.0,
        }

        for category, flagged in result.categories.model_dump().items():
            safety_result["categories"][category] = flagged

        for category, score in result.category_scores.model_dump().items():
            safety_result["category_scores"][category] = score

        results.append(safety_result)

    return results


def check_document_sections_safety(
    sections: Dict[str, str],
) -> Dict[str, Dict[str, Any]]:
    """
    Check safety of different document sections.

    Args:
        sections: Dictionary mapping section names to text

    Returns:
        Dictionary mapping section names to safety results
    """
    import openai

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))

    section_results = {}

    for section_name, section_text in sections.items():
        if section_text.strip():
            response = client.moderations.create(
                input=section_text, model="text-moderation-latest"
            )

            result = response.results[0]

            safety_result = {
                "flagged": result.flagged,
                "categories": {},
                "category_scores": {},
                "overall_score": max(result.category_scores.values())
                if result.category_scores
                else 0.0,
            }

            for category, flagged in result.categories.model_dump().items():
                safety_result["categories"][category] = flagged

            for category, score in result.category_scores.model_dump().items():
                safety_result["category_scores"][category] = score

            section_results[section_name] = safety_result
        else:
            section_results[section_name] = {
                "flagged": False,
                "categories": {},
                "category_scores": {},
                "overall_score": 0.0,
            }

    return section_results


def get_safety_summary(safety_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a summary of safety analysis results.

    Args:
        safety_results: Safety analysis results from check_ocr_text_safety

    Returns:
        Summary dictionary
    """
    flagged_categories = []
    high_risk_categories = []

    for category, flagged in safety_results.get("categories", {}).items():
        if flagged:
            flagged_categories.append(category)
            score = safety_results.get("category_scores", {}).get(category, 0.0)
            if score > 0.7:
                high_risk_categories.append({"category": category, "score": score})

    summary = {
        "is_unsafe": safety_results.get("flagged", False),
        "flagged_categories": flagged_categories,
        "high_risk_categories": high_risk_categories,
        "overall_risk_score": safety_results.get("overall_score", 0.0),
        "risk_level": "high" if safety_results.get("flagged", False) else "low",
    }

    if safety_results.get("flagged", False):
        if safety_results.get("overall_score", 0.0) > 0.9:
            summary["risk_level"] = "critical"
        elif safety_results.get("overall_score", 0.0) > 0.7:
            summary["risk_level"] = "high"
        else:
            summary["risk_level"] = "medium"

    return summary


def filter_unsafe_content(text: str, safety_results: Dict[str, Any]) -> str:
    """
    Filter or redact unsafe content from text based on safety analysis.

    Args:
        text: Original text
        safety_results: Safety analysis results

    Returns:
        Filtered text with unsafe content redacted
    """
    if not safety_results.get("flagged", False):
        return text

    import re

    filtered_text = text

    high_risk_categories = []
    for category, flagged in safety_results.get("categories", {}).items():
        if flagged:
            score = safety_results.get("category_scores", {}).get(category, 0.0)
            if score > 0.7:
                high_risk_categories.append(category)

    if high_risk_categories:
        lines = filtered_text.split("\n")
        filtered_lines = []

        for line in lines:
            line_safety = check_ocr_text_safety(line)
            if line_safety.get("flagged", False):
                filtered_lines.append("[CONTENT REDACTED]")
            else:
                filtered_lines.append(line)

        filtered_text = "\n".join(filtered_lines)

    return filtered_text
