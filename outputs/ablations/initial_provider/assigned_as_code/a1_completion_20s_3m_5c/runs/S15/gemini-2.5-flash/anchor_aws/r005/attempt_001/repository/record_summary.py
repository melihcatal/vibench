import os
from database_client import get_comprehend_client
from database_models import Document

def summarize_record(document: Document, text_field: str, region_name: str = None):
    region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
    comprehend = get_comprehend_client(region_name=region_name)

    text_to_analyze = document.get(text_field, "")
    if not text_to_analyze:
        return {"summary": "No text field to summarize."}

    # Detect dominant language first, as other operations require it
    language_response = comprehend.detect_dominant_language(Text=text_to_analyze)
    languages = language_response.get("Languages", [])
    dominant_language = languages[0]["LanguageCode"] if languages else "en"

    # Using key phrases and sentiment as a form of summarization
    key_phrases_response = comprehend.detect_key_phrases(
        Text=text_to_analyze,
        LanguageCode=dominant_language
    )
    sentiment_response = comprehend.detect_sentiment(
        Text=text_to_analyze,
        LanguageCode=dominant_language
    )

    summary_data = {
        "language": dominant_language,
        "sentiment": sentiment_response.get("Sentiment"),
        "key_phrases": [phrase["Text"] for phrase in key_phrases_response.get("KeyPhrases", [])]
    }
    return {"summary": summary_data}
