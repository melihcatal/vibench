import boto3

class DocumentClient:
    def __init__(self, region_name='us-east-1'):
        self.client = boto3.client('textract', region_name=region_name)

    def analyze_document(self, document_bytes):
        response = self.client.analyze_document(
            Document={'Bytes': document_bytes},
            FeatureTypes=['TABLES', 'FORMS']
        )
        return response
