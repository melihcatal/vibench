import os

from amazon.textract import TextractClient


class DocumentClient:
    def __init__(self):
        self.textract_client = TextractClient(
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-west-2')
        )

    def extract_document(self, document):
        return self.textract_client.analyze_document(document)


def get_document_client():
    return DocumentClient()
