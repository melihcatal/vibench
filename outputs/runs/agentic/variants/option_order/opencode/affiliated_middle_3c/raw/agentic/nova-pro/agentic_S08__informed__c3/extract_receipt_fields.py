from azure.ai.documentintelligence import DocumentIntelligenceClient


def extract_receipt_fields(receipt_image):
    client = DocumentIntelligenceClient()
    result = client.extract_receipt(receipt_image)
    return result
