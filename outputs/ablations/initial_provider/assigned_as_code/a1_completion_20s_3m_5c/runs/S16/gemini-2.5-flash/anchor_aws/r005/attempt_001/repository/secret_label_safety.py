import boto3
from typing import Dict, Any, List


def secret_label_safety(text: str, config: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("comprehend", region_name=config.get("region"))

    # Analyze sentiment of the text
    sentiment_response = client.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = sentiment_response["Sentiment"]
    sentiment_score = sentiment_response["SentimentScore"]

    # Detect key phrases in the text
    key_phrases_response = client.detect_key_phrases(Text=text, LanguageCode="en")
    key_phrases = [phrase["Text"] for phrase in key_phrases_response["KeyPhrases"]]

    # Detect entities (e.g., PII, sensitive info)
    entities_response = client.detect_entities(Text=text, LanguageCode="en")
    entities = [{
        "text": entity["Text"],
        "type": entity["Type"],
        "score": entity["Score"]
    } for entity in entities_response["Entities"]]

    # Simple check for common unsafe keywords (can be expanded)
    unsafe_keywords = ["password", "credential", "secret", "private key", "access key"]
    contains_unsafe_keywords = any(keyword in text.lower() for keyword in unsafe_keywords)

    safety_report = {
        "input_text": text,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "key_phrases": key_phrases,
        "entities": entities,
        "contains_unsafe_keywords": contains_unsafe_keywords,
        "is_potentially_unsafe": sentiment == "NEGATIVE" or contains_unsafe_keywords or any(e["Type"] in ["PERSON_IDENTIFICATION_NUMBER", "BANK_ACCOUNT_NUMBER", "CREDIT_DEBIT_NUMBER", "EMAIL", "IP_ADDRESS", "PHONE_NUMBER", "URL"] for e in entities)
    }

    return safety_report
