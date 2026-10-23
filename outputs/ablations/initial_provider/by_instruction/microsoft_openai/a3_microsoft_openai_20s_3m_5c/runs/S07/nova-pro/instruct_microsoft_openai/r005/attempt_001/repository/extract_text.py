from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def extract_text(image_path):
    client = DocumentIntelligenceClient(endpoint='https://<your-resource-name>.cognitiveservices.azure.com/', credential=AzureKeyCredential('<your-api-key>'))
    with open(image_path, 'rb') as image_data:
        poller = client.begin_analyze_document('prebuilt-document', document=image_data, reading_order='natural')
        result = poller.result()
        return result.content
