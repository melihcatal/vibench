from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def secret_label_safety(label):
    credential = AzureKeyCredential("<your-text-analytics-key>")
    client = TextAnalyticsClient(endpoint="https://<your-text-analytics-endpoint>.cognitiveservices.azure.com/", credential=credential)
    result = client.detect_language(documents=[label])
    return result[0].is_error is False