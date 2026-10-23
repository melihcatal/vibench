from google.cloud import secretmanager
from google.cloud import language_v1
from security_client import SecretManagerClient
from security_models import SecretLabelSafetyPayload, LabelSafetyOutput

def secret_label_safety(payload: SecretLabelSafetyPayload) -> LabelSafetyOutput:
    sm_client = SecretManagerClient()
    nl_client = language_v1.LanguageServiceClient()

    secret_id = payload.secret_id
    project_id = payload.project_id

    # Fetch secret metadata to get labels
    secret = sm_client.get_secret(project_id=project_id, secret_id=secret_id)
    labels = secret.labels

    unsafe_labels = {}
    overall_safe = True

    # Simple keyword check for demonstration. A real-world scenario might use NLP for sentiment, PII detection, etc.
    unsafe_keywords = ["password", "credential", "confidential", "private", "danger"]

    for key, value in labels.items():
        text_to_analyze = f"{key}:{value}"
        for keyword in unsafe_keywords:
            if keyword in text_to_analyze.lower():
                unsafe_labels[key] = value
                overall_safe = False
                break
        
        # More advanced: using Natural Language API for sentiment analysis on labels
        # document = language_v1.Document(content=text_to_analyze, type_=language_v1.Document.Type.PLAIN_TEXT)
        # sentiment = nl_client.analyze_sentiment(request={'document': document}).document_sentiment
        # if sentiment.score < -0.5: # Example: very negative sentiment could be unsafe
        #     unsafe_labels[key] = value
        #     overall_safe = False

    # For the 'notes' part, it's not directly available in GCSM API. 
    # If notes were stored as a specific secret version or in a label, we'd retrieve and analyze it.
    # For this example, we'll leave unsafe_notes empty as we don't have a direct 'notes' field.
    unsafe_notes = {}

    return LabelSafetyOutput(
        secret_id=secret_id,
        unsafe_labels=unsafe_labels,
        unsafe_notes=unsafe_notes,
        overall_safe=overall_safe
    )
