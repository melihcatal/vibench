import os
from typing import Any

class StructuredDocumentClient:
    """
    Unified client wrapper for structured document extraction providers.
    The concrete provider is selected via the `service` argument and its
    credentials/environment variables (e.g., AWS_ENDPOINT_URL, GOOGLE_APPLICATION_CREDENTIALS).
    """
    def __init__(self, service: str = "textract") -> None:
        self.service = service
        # Example: AWS Textract, GCP Document AI, Azure Form Recognizer
        if service == "textract":
            import boto3
            self.client = boto3.client("textract")
        elif service == "document_ai":
            from google.cloud import documentai_v1beta3 as documentai
            self.client = documentai.DocumentUnderstandingServiceClient()
        elif service == "form_recognizer":
            from azure.ai.formrecognizer import FormRecognizerClient
            self.client = FormRecognizerClient(endpoint=os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT"), credential=os.getenv("AZURE_FORM_RECOGNIZER_KEY"))
        else:
            raise ValueError(f"Unsupported service: {service}")

    def extract(self, request: Any) -> Any:
        """Delegate extraction to the underlying provider."""
        if self.service == "textract":
            # AWS Textract synchronous API example
            response = self.client.detect_document_text(**request.to_dict())
            return request.response_schema(response)
        elif self.service == "document_ai":
            # GCP Document AI synchronous processing
            parent = "projects/{}/locations/{}".format(
                self.client.project, self.client._transport._host.split(":")[0].split("//")[1]
            )
            response = self.client.process_document(parent=parent, document=request.to_document())
            return request.response_schema(response)
        elif self.service == "form_recognizer":
            poller = self.client.begin_recognize_content(request)
            result = poller.result()
            return request.response_schema(result)
        else:
            raise NotImplementedError()