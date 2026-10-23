from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.ai.textanalytics import TextAnalyticsClient



def summarize_stored_asset(config, object_name):
    with DefaultAzureCredential() as credential:
        storage_client = BlobServiceClient(config['account_url'], credential=credential)
        blob = storage_client.get_blob_client(container=config['container'], blob=object_name)
        image_data = blob.download_blob().readall()

        text_analytics_client = TextAnalyticsClient(endpoint=config['text_analytics_endpoint'], credential=credential)
        result = text_analytics_client.summarize(documents=[image_data])

        if result[0].sentences:
            return {'summary': ' '.join([sentence.text for sentence in result[0].sentences])}
        else:
            return {'error': 'Summarization failed'}