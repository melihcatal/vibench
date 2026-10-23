import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')

text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))

documents = ["This is a log message to embed."]
response = text_analytics_client.extract_key_phrases(documents)
for document in response:
    print(document.key_phrases)