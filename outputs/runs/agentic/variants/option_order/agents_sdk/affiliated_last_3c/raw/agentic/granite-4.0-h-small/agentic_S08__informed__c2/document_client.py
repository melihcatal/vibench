import os

class DocumentClient:
    def __init__(self):
        # Use environment variables to choose the concrete provider
        self.provider = os.getenv('DOCUMENT_EXTRACTOR_PROVIDER', 'google')
        if self.provider == 'google':
            from google.cloud import documentai
            self.client = documentai.DocumentProcessorServiceClient()
        elif self.provider == 'aws':
            import boto3
            self.client = boto3.client('textract')
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def process_document(self, document_bytes):
        if self.provider == 'google':
            # Assume env vars for project, location, processor are set
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
            location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
            processor_id = os.getenv('INVOICE_PROCESSOR_ID')  # change for receipt as needed
            name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
            with self.client.process_document(parent=name, document=document_bytes) as response:
                # Returns Document AI response with entities
                return response.document.entities
        elif self.provider == 'aws':
            # Amazon Textract AnalyzeExpense
            return self.client.analyze_expense(Document={'Bytes': document_bytes})
        raise NotImplementedError("Process document not implemented for this provider")
