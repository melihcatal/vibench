from typing import List

from safety_client import aws_comprehend_client


def moderation_reason_embedding(text: str) -> List[float]:
    client = aws_comprehend_client("comprehend")
    response = client.detect_syntax(Text=text, LanguageCode="en")
    return [float(token.get("BeginOffset", 0)) for token in response.get("SyntaxTokens", [])]
