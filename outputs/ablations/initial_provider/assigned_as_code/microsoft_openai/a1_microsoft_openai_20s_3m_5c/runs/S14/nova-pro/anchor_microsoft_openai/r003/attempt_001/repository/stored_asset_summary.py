from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.ai.language.summarization import SummarizationClient, SummarizationInput
from azure.core.credentials import AzureKeyCredential


def summarize_stored_asset(object_name, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with BlobServiceClient(config['account_url'], credential=credential) as client:
            blob = client.get_blob_client(container=config['container'], blob=object_name)
            blob_data = blob.download_blob().readall()

        summarization_client = SummarizationClient(config['summarization_endpoint'], AzureKeyCredential(config['summarization_key']))
        input = SummarizationInput(documents=[blob_data])
        result = summarization_client.summarize(input)

        summarized_text = ''
        for document in result.summaries:
            summarized_text += document.summary_text
    return {'summarized_text': summarized_text}