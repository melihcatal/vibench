from azure.ai.textanalytics import TextAnalyticsClient

def stored_asset_summary(container_name: str, blob_name: str):
    client = StorageClient()
    blob_client = client.get_blob_client(container_name, blob_name)
    text_analytics_client = TextAnalyticsClient()
    result = text_analytics_client.summarize(blob_client.download_blob().readall())
    return result.summaries[0].text