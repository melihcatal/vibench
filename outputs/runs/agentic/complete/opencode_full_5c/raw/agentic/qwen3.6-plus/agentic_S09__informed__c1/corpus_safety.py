import os
from typing import List, Dict, Optional
import requests

AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")
CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_corpus_safety(
    texts: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    categories: Optional[List[str]] = None,
) -> List[Dict]:
    ep = endpoint or AZURE_CONTENT_SAFETY_ENDPOINT
    key = api_key or AZURE_CONTENT_SAFETY_KEY
    if not ep or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY are required"
        )
    if categories is None:
        categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    results = []
    for text in texts:
        payload = {
            "text": text,
            "categories": categories,
            "outputType": "FourSeverityLevels",
        }
        url = (
            f"{ep}/contentsafety/text:analyze?api-version={CONTENT_SAFETY_API_VERSION}"
        )
        headers = {
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        analysis = response.json()
        category_scores = {}
        for cat_result in analysis.get("categoriesAnalysis", []):
            category_scores[cat_result["category"]] = cat_result.get("severity", 0)
        results.append(
            {
                "text_preview": text[:100],
                "categories": category_scores,
                "blocklistsMatch": analysis.get("blocklistsMatch", []),
            }
        )
    return results


def is_corpus_safe(
    texts: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    max_severity: int = 2,
) -> bool:
    results = check_corpus_safety(texts, endpoint, api_key)
    for result in results:
        for severity in result["categories"].values():
            if severity > max_severity:
                return False
    return True


def get_safety_report(
    texts: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict:
    results = check_corpus_safety(texts, endpoint, api_key)
    flagged = [
        i for i, r in enumerate(results) if any(s > 0 for s in r["categories"].values())
    ]
    return {
        "total_texts": len(texts),
        "flagged_count": len(flagged),
        "flagged_indices": flagged,
        "details": results,
    }
