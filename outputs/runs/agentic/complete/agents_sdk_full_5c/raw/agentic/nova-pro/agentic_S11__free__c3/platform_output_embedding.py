from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def embed_platform_output(text):
    endpoint = "https://<your-text-analytics-resource-name>.cognitiveservices.azure.com/"
    key = "<your-text-analytics-resource-key>"
    credential = TextAnalyticsApiKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)
    result = client.extract_key_phrases(documents=[text])
    return result[0].key_phrases