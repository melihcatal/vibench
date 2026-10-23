from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def log_message_translate(log_text, target_language, config):
    credential = AzureKeyCredential(config['text_analytics_key'])
    client = TextAnalyticsClient(endpoint=config['text_analytics_endpoint'], credential=credential)
    result = client.translate(documents=[log_text], to=target_language)[0]
    return result.translations[0].text