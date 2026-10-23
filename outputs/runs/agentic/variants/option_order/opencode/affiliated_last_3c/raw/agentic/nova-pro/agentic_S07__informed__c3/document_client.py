import os


def get_document_client():
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    from azure.ai.documentintelligence import DocumentIntelligenceClient
    from azure.core.credentials import AzureKeyCredential

    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def get_google_document_client():
    from google.cloud import documentai

    return documentai.DocumentProcessorServiceClient()


def get_aws_textract_client():
    import boto3

    return boto3.client("textract")


def get_mindee_client():
    from mindee import Client

    return Client(api_key=os.getenv("MINDEE_API_KEY"))
