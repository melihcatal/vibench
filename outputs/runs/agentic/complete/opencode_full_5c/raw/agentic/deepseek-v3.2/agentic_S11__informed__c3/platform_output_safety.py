import requests
import os
from typing import Dict, Any, List, Optional


def check_content_safety_perspective(
    text: str, languages: List[str] = None
) -> Dict[str, Any]:
    """
    Check platform model output for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    requested_attributes = {
        "TOXICITY": {},
        "SEVERE_TOXICITY": {},
        "IDENTITY_ATTACK": {},
        "INSULT": {},
        "PROFANITY": {},
        "THREAT": {},
        "SEXUALLY_EXPLICIT": {},
        "FLIRTATION": {},
    }

    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": languages or ["en"],
        "doNotStore": True,
    }

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        result = response.json()

        attribute_scores = result.get("attributeScores", {})

        safety_scores = {}
        for attr_name, attr_data in attribute_scores.items():
            summary_score = attr_data.get("summaryScore", {})
            safety_scores[attr_name] = {
                "score": summary_score.get("value", 0),
                "type": summary_score.get("type", "PROBABILITY"),
            }

        max_score = 0
        highest_risk = None
        for attr_name, scores in safety_scores.items():
            if scores["score"] > max_score:
                max_score = scores["score"]
                highest_risk = attr_name

        is_safe = max_score < 0.7

        return {
            "text": text,
            "is_safe": is_safe,
            "highest_risk": highest_risk,
            "highest_risk_score": max_score,
            "safety_scores": safety_scores,
            "languages_checked": languages or ["en"],
            "provider": "perspective_api",
            "raw_response": result,
        }

    except requests.exceptions.RequestException as e:
        return {
            "text": text,
            "error": str(e),
            "is_safe": False,
            "provider": "perspective_api",
        }


def check_batch_safety(
    texts: List[str], languages: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Check multiple texts for safety.
    """
    results = []
    for text in texts:
        results.append(check_content_safety_perspective(text, languages))
    return results


def get_safety_summary(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate summary statistics from safety check results.
    """
    total = len(results)
    safe_count = sum(1 for r in results if r.get("is_safe", False))
    unsafe_count = total - safe_count

    risk_distribution = {}
    for result in results:
        highest_risk = result.get("highest_risk")
        if highest_risk:
            risk_distribution[highest_risk] = risk_distribution.get(highest_risk, 0) + 1

    avg_scores = {}
    for result in results:
        safety_scores = result.get("safety_scores", {})
        for attr_name, scores in safety_scores.items():
            if attr_name not in avg_scores:
                avg_scores[attr_name] = []
            avg_scores[attr_name].append(scores["score"])

    avg_scores_summary = {}
    for attr_name, scores in avg_scores.items():
        avg_scores_summary[attr_name] = sum(scores) / len(scores)

    return {
        "total_texts": total,
        "safe_texts": safe_count,
        "unsafe_texts": unsafe_count,
        "safety_rate": safe_count / total if total > 0 else 0,
        "risk_distribution": risk_distribution,
        "average_scores": avg_scores_summary,
        "provider": "perspective_api",
    }
