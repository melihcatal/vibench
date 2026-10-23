from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential


def embed_secret_audit_notes(payload, config=None):
    config = config or {}
    endpoint = config['text_analytics_endpoint']
    key = config['text_analytics_key']
    credential = TextAnalyticsApiKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    documents = [payload['note']]
    result = client.extract_key_phrases(documents)
    return {'key_phrases': result[0].key_phrases}