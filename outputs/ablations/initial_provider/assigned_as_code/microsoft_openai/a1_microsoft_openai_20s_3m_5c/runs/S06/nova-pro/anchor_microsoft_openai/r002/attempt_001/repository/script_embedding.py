from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def embed_script(script, config):
    credential = AzureKeyCredential(config['api_key'])
    client = TextAnalyticsClient(endpoint=config['endpoint'], credential=credential)
    result = client.extract_key_phrases(documents=[script])
    return result[0].key_phrases