import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

def summarize_invoice(invoice_text):
    client = TextAnalyticsClient(
        endpoint=os.getenv('TEXT_ANALYTICS_ENDPOINT'),
        credential=TextAnalyticsApiKeyCredential(os.getenv('TEXT_ANALYTICS_KEY'))
    )
    result = client.summarize(invoice_text, max_sentence_count=3)
    return result[0].sentences[0]