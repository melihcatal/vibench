from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials


def translate_stored_text(config, object_name, target_language):
    credential = DefaultAzureCredential()
    blob_client = BlobServiceClient(config['account_url'], credential=credential)
    blob = blob_client.get_blob_client(container=config['container'], blob=object_name)
    download_stream = blob.download_blob()
    text_analytics_client = TextAnalyticsClient(config['textanalytics_endpoint'], CognitiveServicesCredentials(config['textanalytics_key']))
    translated_text = text_analytics_client.translate(download_stream.content_as_text(), target_language)
    return translated_text
