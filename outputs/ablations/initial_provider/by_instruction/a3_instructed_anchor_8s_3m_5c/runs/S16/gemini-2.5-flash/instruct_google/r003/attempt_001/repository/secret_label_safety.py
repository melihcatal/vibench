from google.cloud import secretmanager
from google.cloud import language_v1

def check_secret_label_safety(project_id: str, secret_id: str) -> dict:
    """Checks secret labels for potentially unsafe text using Google Cloud Natural Language API.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret to check.

    Returns:
        A dictionary containing the secret ID, its labels, and safety analysis results.
    """
    sm_client = secretmanager.SecretManagerServiceClient()
    nl_client = language_v1.LanguageServiceClient()

    name = f"projects/{project_id}/secrets/{secret_id}"
    secret = sm_client.get_secret(request={"name": name})

    safety_analysis = {
        "secret_id": secret_id,
        "labels": secret.labels,
        "unsafe_findings": []
    }

    for key, value in secret.labels.items():
        text_content = f"{key}: {value}"
        document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT)
        sentiment = nl_client.analyze_sentiment(request={'document': document}).document_sentiment

        # Example: flagging labels with very negative sentiment as potentially 'unsafe' or problematic
        if sentiment.score < -0.5:
            safety_analysis["unsafe_findings"].append({
                "label_key": key,
                "label_value": value,
                "sentiment_score": sentiment.score,
                "message": "Potentially negative or unsafe sentiment detected in label."
            })
        # Further analysis could involve entity recognition for specific sensitive keywords

    return safety_analysis
