import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.formrecognizer.models import AnalyzeDocumentRequest

def extract_fields(text):
    client = DocumentAnalysisClient(endpoint=os.getenv('AZURE_FORM_RECOGNIZER_ENDPOINT'), credential=os.getenv('AZURE_FORM_RECOGNIZER_KEY'))
    poller = client.begin_analyze_document('prebuilt-document', AnalyzeDocumentRequest(document=text))
    result = poller.result()
    fields = {field.name: field.value for field in result.fields}
    return fields