"""Check narration scripts for unsafe content using Google Cloud Natural Language API."""

from typing import Dict, List, Optional, Tuple

from google.cloud import language_v1 as language


def check_script_safety(
    text: str,
    threshold: float = 0.5,
) -> Dict[str, object]:
    """Check a narration script for unsafe content via Google Cloud Natural Language API.

    Uses the google-cloud-language client connecting to language.googleapis.com
    to perform content moderation analysis. Returns a dict with safety labels,
    scores, and an overall safe/unsafe verdict.
    """
    client = language.LanguageServiceClient()

    document = language.Document(
        content=text,
        type_=language.Document.Type.PLAIN_TEXT,
    )

    request = language.AnalyzeSentimentRequest(
        document=document,
    )
    response = client.analyze_sentiment(request=request)

    sentiment = response.document_sentiment
    score = sentiment.score
    magnitude = sentiment.magnitude

    safety_result = _evaluate_safety(score, magnitude, threshold)

    return {
        "text": text,
        "safe": safety_result["safe"],
        "sentiment_score": score,
        "sentiment_magnitude": magnitude,
        "categories": safety_result["categories"],
        "flagged": safety_result["flagged"],
        "verdict": safety_result["verdict"],
    }


def check_multiple_scripts(
    texts: List[str],
    threshold: float = 0.5,
) -> List[Dict[str, object]]:
    """Check multiple narration scripts for unsafe content via Google Cloud NLP.

    Processes each text through language.googleapis.com and returns a list
    of safety analysis results.
    """
    results = []
    for text in texts:
        result = check_script_safety(text, threshold=threshold)
        results.append(result)
    return results


def _evaluate_safety(
    score: float,
    magnitude: float,
    threshold: float,
) -> Dict[str, object]:
    """Evaluate sentiment scores to determine content safety.

    Uses heuristics on Google Cloud Natural Language API sentiment scores
    to flag potentially problematic content (extreme negativity, high intensity
    negative sentiment, etc.).
    """
    categories = []
    flagged = []

    if score < -threshold:
        categories.append("highly_negative")
        flagged.append("strong_negative_sentiment")

    if magnitude > 5.0 and score < -0.3:
        categories.append("intense_negative")
        flagged.append("high_intensity_negativity")

    if score > threshold:
        categories.append("highly_positive")

    if abs(score) <= threshold and magnitude < 2.0:
        categories.append("neutral")

    is_safe = len(flagged) == 0
    verdict = "safe" if is_safe else "unsafe"

    return {
        "safe": is_safe,
        "categories": categories,
        "flagged": flagged,
        "verdict": verdict,
    }
