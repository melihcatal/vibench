import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')

text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))

documents = ["This is a safe log message.", "This log message contains profanity."]
response = text_analytics_client.analyze_sentiment(documents)
for document in response:
    print(document.sentiment)