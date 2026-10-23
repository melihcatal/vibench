import os

# This file provides local configuration and client helper utilities for Structured Document Extraction.
# It does not directly integrate with a single external provider, but rather helps initialize
# clients for various document processing services based on configuration.


class DocumentClientConfig:
    def __init__(self):
        # Google Document AI
        self.google_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.google_document_ai_location = os.environ.get(
            "GOOGLE_DOCUMENT_AI_LOCATION", "us"
        )
        self.google_invoice_processor_id = os.environ.get(
            "DOCUMENT_AI_INVOICE_PROCESSOR_ID"
        )

        # Amazon Textract
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.environ.get("AWS_REGION", "us-east-1")

        # Other API keys (e.g., for LLMs, Content Safety, etc.)
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        self.azure_content_safety_endpoint = os.environ.get(
            "AZURE_CONTENT_SAFETY_ENDPOINT"
        )
        self.azure_content_safety_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
        self.perspective_api_key = os.environ.get("PERSPECTIVE_API_KEY")
        self.deepl_auth_key = os.environ.get(
            "DEEPL_AUTH_KEY"
        )  # For translation, will use Google Cloud Translation though
        self.google_cloud_translate_project_id = os.environ.get(
            "GOOGLE_CLOUD_PROJECT"
        )  # Reusing for translation


def get_document_ai_client(location: str = None):
    """
    Returns a Google Document AI client. (Imported in extract_invoice_fields directly)
    This is a placeholder as the client is directly initialized where used to demonstrate provider integration.
    """
    # from google.cloud import documentai_v1beta3 as documentai
    # from google.api_core.client_options import ClientOptions
    # opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    # return documentai.DocumentProcessorServiceClient(client_options=opts)
    pass


def get_textract_client(region_name: str = None):
    """
    Returns an Amazon Textract client. (Imported in extract_receipt_fields directly)
    This is a placeholder as the client is directly initialized where used to demonstrate provider integration.
    """
    # import boto3
    # return boto3.client('textract', region_name=region_name)
    pass


# Additional helper functions could be added here for common client initialization patterns

if __name__ == "__main__":
    config = DocumentClientConfig()
    print("Document Client Configuration Loaded:")
    print(f"  Google Project ID: {config.google_project_id}")
    print(f"  AWS Region: {config.aws_region}")
    print(f"  Google API Key (exists): {'Yes' if config.google_api_key else 'No'}")
