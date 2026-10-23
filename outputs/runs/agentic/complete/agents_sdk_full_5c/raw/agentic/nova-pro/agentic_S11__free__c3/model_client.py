from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def get_text_analytics_client():
    endpoint = "https://<your-text-analytics-resource-name>.cognitiveservices.azure.com/"
    key = "<your-text-analytics-resource-key>"
    credential = TextAnalyticsApiKeyCredential(key)
    return TextAnalyticsClient(endpoint=endpoint, credential=credential)