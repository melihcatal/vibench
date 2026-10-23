from google.cloud import language_v1
from typing import List, Dict

def summarize_quality_issues(translated_texts: List[str], target_language: str) -> Dict[str, List[str]]:
    """Summarizes potential translation quality issues using Google Cloud Natural Language API for sentiment analysis.

    This function aims to identify translations that might have negative sentiment,
    which could indicate a quality issue or a mistranslation that alters the original tone.

    Args:
        translated_texts: A list of translated text segments.
        target_language: The language of the translated texts.

    Returns:
        A dictionary summarizing potential quality issues, categorizing texts with negative sentiment.
    """
    client = language_v1.LanguageServiceClient()
    issues = {
        "negative_sentiment_translations": [],
        "neutral_sentiment_translations": [],
        "positive_sentiment_translations": [],
    }

    for text in translated_texts:
        document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language=target_language)
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

        if sentiment.score < -0.25:  # Arbitrary threshold for negative sentiment
            issues["negative_sentiment_translations"].append(text)
        elif sentiment.score > 0.25: # Arbitrary threshold for positive sentiment
            issues["positive_sentiment_translations"].append(text)
        else:
            issues["neutral_sentiment_translations"].append(text)

    return issues
