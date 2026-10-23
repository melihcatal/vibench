from google.cloud import language_v1 as language
from typing import List, Dict

def check_script_safety(text: str) -> Dict[str, List[Dict]]:
    client = language.LanguageServiceClient()
    document = language.Document(
        content=text,
        type_=language.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_sentiment(
        request={"document": document}
    )
    sentiment = response.document_sentiment
    
    response_categories = client.classify_text(
        request={"document": document}
    )
    categories = [
        {"name": category.name, "confidence": category.confidence}
        for category in response_categories.categories
    ]
    
    return {
        "sentiment": {
            "score": sentiment.score,
            "magnitude": sentiment.magnitude
        },
        "categories": categories
    }