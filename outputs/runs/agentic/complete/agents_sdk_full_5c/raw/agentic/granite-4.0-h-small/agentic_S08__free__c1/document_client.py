import os

class DocumentClient:
    """
    Centralized client configuration and helper utilities for Structured Document Extraction.
    Abstracts provider-specific initialisation so downstream modules can import a single helper.
    """

    PROVIDER = os.getenv("DOC_PROVIDER", "gcp")

    @staticmethod
    def get_extractor(provider: str = None) -> Any:
        """Return a configured extractor instance based on environment or argument."""
        provider = provider or DocumentClient.PROVIDER
        if provider.lower() == "gcp":
            from .extract_invoice_fields import InvoiceExtractor
            # Environment variables must be set:
            #   GOOGLE_PROJECT_ID, GOOGLE_INVOICE_PROCESSOR_ID
            return InvoiceExtractor(
                project_id=os.getenv("GOOGLE_PROJECT_ID"),
                processor_id=os.getenv("GOOGLE_INVOICE_PROCESSOR_ID"),
            )
        elif provider.lower() == "aws":
            from .extract_receipt_fields import ReceiptExtractor
            return ReceiptExtractor(region_name=os.getenv("AWS_REGION", "us-east-1"))
        else:
            raise ValueError(f"Unsupported provider: {provider}")
