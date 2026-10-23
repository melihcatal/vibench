import boto3

class DocumentClient:
    def __init__(self, region_name):
        self.client = boto3.client("textract", region_name=region_name)

    def get_textract_client(self):
        return self.client
