from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def incident_summary(payload, config=None):
    config = config or {}
    endpoint = config["endpoint"]
    key = config["key"]
    documents = [row.get("Message", "") for row in payload.get("rows", []) if row.get("Message")]
    if not documents:
        return {"summary": "No incident evidence provided.", "severity": "unknown"}
    client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    extracted = client.extract_key_phrases(documents)
    phrases = []
    for doc in extracted:
        if not doc.is_error:
            phrases.extend(doc.key_phrases)
    return {"summary": "; ".join(sorted(set(phrases))[:10]), "severity": payload.get("severity", "error")}
