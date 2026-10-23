from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def secret_audit_embedding(notes):
    credential = AzureKeyCredential("<your-text-analytics-key>")
    client = TextAnalyticsClient(endpoint="https://<your-text-analytics-endpoint>.cognitiveservices.azure.com/", credential=credential)
    result = client.extract_key_phrases(documents=[notes])
    return result[0].key_phrases