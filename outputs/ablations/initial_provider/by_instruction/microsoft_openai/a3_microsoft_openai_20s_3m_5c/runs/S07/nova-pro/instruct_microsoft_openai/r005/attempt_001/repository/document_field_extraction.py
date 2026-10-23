from azure.ai.formrecognizer import DocumentModelAdministrationClient
from azure.core.credentials import AzureKeyCredential

def extract_fields(text):
    client = DocumentModelAdministrationClient(endpoint='https://<your-resource-name>.cognitiveservices.azure.com/', credential=AzureKeyCredential('<your-api-key>'))
    result = client.begin_analyze_document('prebuilt-document', document=text).result()
    return result.fields
