from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials


def log_embedding(log_text, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        client = TextAnalyticsClient(endpoint=config['endpoint'], credentials=CognitiveServicesCredentials(credential.get_token('https://api.cognitive.microsoft.com/sts/v1.0/issueToken').token))
        embeddings = client.extract_key_phrases(documents=[log_text])[0].key_phrases
        return embeddings
