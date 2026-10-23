from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def select_platform_resource():
    endpoint = "https://<your-text-analytics-resource-name>.cognitiveservices.azure.com/"
    key = "<your-text-analytics-resource-key>"
    credential = TextAnalyticsApiKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    return client