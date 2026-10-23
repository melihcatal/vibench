from azure.ai.documentintelligence import DocumentIntelligenceClient


def extract_receipt_fields(receipt_image):
    client = DocumentIntelligenceClient(
        AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
    )
    response = client.extract_receipt(receipt_image)
    return response
