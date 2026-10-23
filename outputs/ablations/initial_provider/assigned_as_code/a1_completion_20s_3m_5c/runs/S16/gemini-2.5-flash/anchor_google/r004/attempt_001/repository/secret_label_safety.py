from google.cloud import language_v2
from security_client import get_natural_language_client
from security_models import SafetyCheckResult

def check_secret_label_safety(text: str, project_id: str):
    client = get_natural_language_client()

    document = language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)
    
    # Using analyze_sentiment as a proxy for safety check. 
    # A more robust safety check would involve custom classification or entity analysis for PII/sensitive terms.
    response = client.analyze_sentiment(request={
        "document": document,
        "encoding_type": language_v2.EncodingType.UTF8,
    })

    unsafe_found = False
    details = []

    # Example heuristic: if sentiment score is very negative, it might indicate unsafe language.
    # This is a very simplified approach for demonstration.
    if response.document_sentiment.score < -0.5:
        unsafe_found = True
        details.append(f"Negative sentiment detected (score: {response.document_sentiment.score})")

    return SafetyCheckResult(unsafe_text_found=unsafe_found, details=details).__dict__
