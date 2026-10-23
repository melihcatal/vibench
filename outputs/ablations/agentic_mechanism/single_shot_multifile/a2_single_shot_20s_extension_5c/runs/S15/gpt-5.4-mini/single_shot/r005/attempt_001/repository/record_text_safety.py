from typing import Any, Dict, List
import boto3

comprehend = boto3.client("comprehend")


def check_text_safety(payload: Dict[str, Any]) -> Dict[str, Any]:
    texts: List[str] = [str(v) for v in payload.get("texts", [])]
    findings = []
    for text in texts:
        res = comprehend.detect_sentiment(Text=text[:5000], LanguageCode=payload.get("language_code", "en"))
        findings.append({"text": text, "sentiment": res.get("Sentiment"), "sentiment_score": res.get("SentimentScore", {})})
    return {"ok": True, "findings": findings}


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    return check_text_safety(event)
