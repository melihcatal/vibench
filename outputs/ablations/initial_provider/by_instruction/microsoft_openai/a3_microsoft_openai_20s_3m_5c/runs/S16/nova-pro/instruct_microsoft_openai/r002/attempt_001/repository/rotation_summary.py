from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def rotation_summary(secret_name):
    credential = AzureKeyCredential("<your-text-analytics-key>")
    client = TextAnalyticsClient(endpoint="https://<your-text-analytics-endpoint>.cognitiveservices.azure.com/", credential=credential)
    result = client.analyze_sentiment(documents=[secret_name])
    return result[0].sentiment