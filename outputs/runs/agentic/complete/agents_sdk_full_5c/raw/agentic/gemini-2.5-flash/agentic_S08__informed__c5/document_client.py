import os

# This file can be used to hold shared client configurations or instantiated clients.
# For simplicity, clients are instantiated directly in their respective integration files
# using environment variables for credentials. This file would be useful for more complex
# multi-client scenarios or shared retry logic.

class DocumentClientConfig:
    """Holds configuration settings for document processing clients."""
    def __init__(self):
        self.google_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        self.google_location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us")
        self.google_documentai_invoice_processor_id = os.environ.get("GOOGLE_DOCUMENTAI_INVOICE_PROCESSOR_ID")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")

        self.azure_content_safety_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.azure_content_safety_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

        # Add other configurations as needed

    def is_google_docai_configured(self) -> bool:
        return all([self.google_project_id, self.google_documentai_invoice_processor_id])

    def is_aws_textract_configured(self) -> bool:
        return all([self.aws_access_key_id, self.aws_secret_access_key, self.aws_region_name])

    def is_google_gemini_configured(self) -> bool:
        return bool(self.google_api_key)

    def is_azure_content_safety_configured(self) -> bool:
        return all([self.azure_content_safety_endpoint, self.azure_content_safety_key])


# Example of a simple shared utility function (not a client directly)
def load_document_content(file_path: str) -> bytes:
    """Loads content of a document from the given file path."""
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return b""

