import boto3

class DocumentClientHelper:
    """
    Provides helper utilities for structured document extraction clients.
    Encapsulates client initialization for various providers.
    """
    def __init__(self, aws_region: str = 'us-east-1'):
        self.aws_region = aws_region

    def get_aws_textract_client(self):
        """
        Returns an initialized AWS Textract client.
        """
        return boto3.client('textract', region_name=self.aws_region)

    # Potentially add other client initializations here for other providers
    # def get_google_documentai_client(self):
    #     # Example for Google Cloud Document AI
    #     from google.cloud import documentai_v1 as documentai
    #     return documentai.DocumentProcessorServiceClient()
