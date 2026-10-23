import os
from google.cloud import language_v1
from security_client import SecurityClient

def analyze_sentiment_of_text(text_content: str) -> dict:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
    return {"score": sentiment.score, "magnitude": sentiment.magnitude}

def check_secret_label_safety(project_id: str, secret_id: str) -> dict:
    client = SecurityClient()
    secret_metadata = client.get_secret_metadata(project_id, secret_id)
    safety_analysis = {}
    for label_key, label_value in secret_metadata.labels.items():
        combined_text = f"{label_key} {label_value}"
        sentiment_result = analyze_sentiment_of_text(combined_text)
        safety_analysis[label_key] = sentiment_result
    return safety_analysis

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_to_check_id = "my-api-key"
    # safety_report = check_secret_label_safety(project_id, secret_to_check_id)
    # print(f"Secret Label Safety Report for {secret_to_check_id}: {safety_report}")
