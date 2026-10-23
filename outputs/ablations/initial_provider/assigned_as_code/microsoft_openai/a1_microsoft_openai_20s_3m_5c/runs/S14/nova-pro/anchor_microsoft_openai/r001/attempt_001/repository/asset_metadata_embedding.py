from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.ai.textanalytics import TextAnalyticsClient



def embed_asset_metadata_and_text(config, object_name):
    with DefaultAzureCredential() as credential:
        storage_client = BlobServiceClient(config['account_url'], credential=credential)
        blob = storage_client.get_blob_client(container=config['container'], blob=object_name)
        image_data = blob.download_blob().readall()

        text_analytics_client = TextAnalyticsClient(endpoint=config['text_analytics_endpoint'], credential=credential)
        result = text_analytics_client.extract_key_phrases(documents=[image_data])

        if result[0].key_phrases:
            return {'key_phrases': result[0].key_phrases}
        else:
            return {'error': 'Key phrase extraction failed'}