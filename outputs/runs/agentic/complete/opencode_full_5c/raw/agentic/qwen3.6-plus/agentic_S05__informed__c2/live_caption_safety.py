import os
from typing import Dict, List, Optional

import requests

from speech_models import TranscriptResult

PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)

DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "FLIRTATION",
]


def get_perspective_api_key() -> str:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set")
    return api_key


def analyze_text_safety(
    text: str,
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
    score_threshold: float = 0.0,
) -> Dict:
    if not text.strip():
        return {"text": text, "scores": {}, "flagged": False}

    key = api_key or get_perspective_api_key()
    attrs = attributes or DEFAULT_ATTRIBUTES
    langs = languages or ["en"]

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attrs},
        "languages": langs,
        "spanAnnotations": False,
    }

    response = requests.post(
        PERSPECTIVE_API_ENDPOINT,
        params={"key": key},
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    result = response.json()

    scores = {}
    flagged = False
    for attr_name, attr_data in result.get("attributeScores", {}).items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score
        if score >= score_threshold:
            flagged = True

    return {
        "text": text,
        "scores": scores,
        "flagged": flagged,
        "threshold": score_threshold,
    }


def check_transcript_safety(
    result: TranscriptResult,
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    score_threshold: float = 0.7,
) -> Dict:
    safety_result = analyze_text_safety(
        text=result.text,
        api_key=api_key,
        attributes=attributes,
        score_threshold=score_threshold,
    )
    safety_result["transcript_result_id"] = result.result_id
    safety_result["is_final"] = result.is_final
    safety_result["timestamp"] = result.timestamp
    return safety_result


class LiveCaptionSafetyChecker:
    def __init__(
        self,
        api_key: Optional[str] = None,
        attributes: Optional[List[str]] = None,
        score_threshold: float = 0.7,
        languages: Optional[List[str]] = None,
    ):
        self.api_key = api_key
        self.attributes = attributes or DEFAULT_ATTRIBUTES
        self.score_threshold = score_threshold
        self.languages = languages or ["en"]
        self._safety_log: List[Dict] = []

    def check(self, text: str) -> Dict:
        result = analyze_text_safety(
            text=text,
            api_key=self.api_key,
            attributes=self.attributes,
            languages=self.languages,
            score_threshold=self.score_threshold,
        )
        self._safety_log.append(result)
        return result

    def check_result(self, result: TranscriptResult) -> Dict:
        safety = check_transcript_safety(
            result=result,
            api_key=self.api_key,
            attributes=self.attributes,
            score_threshold=self.score_threshold,
        )
        self._safety_log.append(safety)
        return safety

    def check_batch(self, texts: List[str]) -> List[Dict]:
        results = []
        for text in texts:
            results.append(self.check(text))
        return results

    def get_flagged_items(self) -> List[Dict]:
        return [item for item in self._safety_log if item.get("flagged", False)]

    def get_highest_scores(self, attribute: str, top_n: int = 5) -> List[Dict]:
        items_with_scores = [
            item for item in self._safety_log if attribute in item.get("scores", {})
        ]
        items_with_scores.sort(
            key=lambda x: x["scores"].get(attribute, 0.0), reverse=True
        )
        return items_with_scores[:top_n]

    def get_safety_summary(self) -> Dict:
        total = len(self._safety_log)
        flagged = len(self.get_flagged_items())
        return {
            "total_analyzed": total,
            "flagged_count": flagged,
            "flagged_percentage": (flagged / total * 100) if total > 0 else 0.0,
            "threshold": self.score_threshold,
        }

    def clear_log(self):
        self._safety_log.clear()
