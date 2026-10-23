from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials


def embed_asset_metadata(config, object_name):
    credential = DefaultAzureCredential()
    blob_client = BlobServiceClient(config['account_url'], credential=credential)
    blob = blob_client.get_blob_client(container=config['container'], blob=object_name)
    download_stream = blob.download_blob()
    text_analytics_client = TextAnalyticsClient(config['textanalytics_endpoint'], CognitiveServicesCredentials(config['textanalytics_key']))
    metadata_embedding = text_analytics_client.embed(download_stream.content_as_text())
    return metadata_embedding
