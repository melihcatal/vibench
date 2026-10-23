import re
from typing import List
from googleapiclient import discovery
from google.api_core.client_options import ClientOptions


def check_text_safety(texts: List[str]) -> List[Dict[str, Any]]:
    """Check corpus texts for safety using Google Cloud's Natural Language API."""
    client_options = ClientOptions(api_endpoint="language.googleapis.com")
    client = discovery.build(
        "language", "v1", client_options=client_options, static_discovery=False
    )

    results = []
    for text in texts:
        if not text.strip():
            results.append({"text": text, "safe": False, "reason": "empty_text"})
            continue

        analyze_request = {
            "document": {"type": "PLAIN_TEXT", "content": text},
            "encodingType": "UTF8",
        }

        try:
            response = (
                client.documents().analyzeSentiment(request=analyze_request).execute()
            )
            sentiment = response.get("documentSentiment", {})

            # Check for toxic content using regex as a fallback
            toxic_patterns = [
                r"\b(?:hate|kill|violence|abuse|racist|sexist|terrorist)\b",
                r"\b(?:fuck|shit|bitch|asshole|dick)\b",
            ]
            is_toxic = any(
                re.search(pattern, text, re.IGNORECASE) for pattern in toxic_patterns
            )

            results.append(
                {
                    "text": text,
                    "safe": not is_toxic and sentiment.get("score", 0) >= -0.8,
                    "reason": "toxic_content"
                    if is_toxic
                    else "negative_sentiment"
                    if sentiment.get("score", 0) < -0.8
                    else "safe",
                }
            )
        except Exception as e:
            results.append({"text": text, "safe": False, "reason": "api_error"})

    return results
