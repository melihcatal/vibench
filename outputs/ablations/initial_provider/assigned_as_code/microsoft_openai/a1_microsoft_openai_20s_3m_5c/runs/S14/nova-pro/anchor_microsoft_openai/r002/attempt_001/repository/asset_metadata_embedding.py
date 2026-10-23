from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials


def embed_asset_metadata(config, object_name, metadata):
    with DefaultAzureCredential() as credential:
        storage_client = BlobServiceClient(config['account_url'], credential=credential)
        blob = storage_client.get_blob_client(container=config['container'], blob=object_name)
        stream = blob.download_blob()
        text = stream.content_as_text()
        text_analytics_client = TextAnalyticsClient(config['textanalytics_endpoint'], CognitiveServicesCredentials(config['textanalytics_key']))
        result = text_analytics_client.analyze_sentiment(text)
        return {'sentiment': result.documents[0].sentiment, 'metadata': metadata}