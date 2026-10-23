from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def stream_platform_generation(text):
    endpoint = "https://<your-text-analytics-resource-name>.cognitiveservices.azure.com/"
    key = "<your-text-analytics-resource-key>"
    credential = TextAnalyticsApiKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    result = client.analyze_sentiment(documents=[text])
    for document in result:
        yield document