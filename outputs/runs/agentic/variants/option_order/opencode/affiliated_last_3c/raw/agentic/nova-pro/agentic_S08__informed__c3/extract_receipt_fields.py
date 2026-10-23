from mindee import Client as MindeeClient
from mindee.documents.base import Document

import os

api_key = os.getenv("MINDEE_API_KEY")


def extract_receipt_fields(image_path):
    client = MindeeClient(api_key)
    document = Document(image_path)
    response = client.receipts.parse(document)
    return response.to_dict()
