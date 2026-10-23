from typing import Iterable

from safety_client import aws_comprehend_client


def moderation_summary(decisions: Iterable[str]) -> str:
    client = aws_comprehend_client("comprehend")
    text = "\n".join(decisions)
    response = client.detect_key_phrases(Text=text, LanguageCode="en")
    phrases = [phrase.get("Text", "") for phrase in response.get("KeyPhrases", [])]
    return "; ".join(phrases)
