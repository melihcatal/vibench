import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

DEFAULT_MODEL_ID = "prebuilt-invoice"
RECEIPT_MODEL_ID = "prebuilt-receipt"
READ_MODEL_ID = "prebuilt-read"


def get_document_analysis_client(model_id=None):
    credential = AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY)
    client = DocumentAnalysisClient(
        endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, credential=credential
    )
    return client


def get_model_id_for_document_type(doc_type):
    mapping = {
        "invoice": DEFAULT_MODEL_ID,
        "receipt": RECEIPT_MODEL_ID,
        "read": READ_MODEL_ID,
    }
    return mapping.get(doc_type, DEFAULT_MODEL_ID)
