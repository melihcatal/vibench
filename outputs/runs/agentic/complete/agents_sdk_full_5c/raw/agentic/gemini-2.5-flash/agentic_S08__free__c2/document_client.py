import os
from google.cloud import documentai_v1 as documentai
from google.cloud import aiplatform
from google.cloud import translate_v3 as translate
from google.cloud import firestore
from google.cloud import dlp_v2 as dlp
import boto3

# Google Cloud Project ID and Location (can be set via environment variables)
PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.environ.get("GCP_LOCATION", "us") # For Document AI, Vertex AI, Translation

# Document AI Processor IDs
INVOICE_PROCESSOR_ID = os.environ.get("DOCUMENTAI_INVOICE_PROCESSOR_ID", f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/your-invoice-processor-id")
RECEIPT_PROCESSOR_ID = os.environ.get("DOCUMENTAI_RECEIPT_PROCESSOR_ID", f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/your-receipt-processor-id")

# AWS Credentials (configured via environment variables or ~/.aws/credentials)
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

class DocumentClients:
    """Manages client instances for various document processing services."""

    _documentai_client = None
    _textract_client = None
    _vertex_ai_prediction_client = None
    _translate_client = None
    _firestore_client = None
    _dlp_client = None

    @classmethod
    def get_documentai_client(cls):
        if cls._documentai_client is None:
            cls._documentai_client = documentai.DocumentProcessorServiceClient()
        return cls._documentai_client

    @classmethod
    def get_textract_client(cls):
        if cls._textract_client is None:
            cls._textract_client = boto3.client("textract", region_name=AWS_REGION)
        return cls._textract_client

    @classmethod
    def get_vertex_ai_prediction_client(cls):
        if cls._vertex_ai_prediction_client is None:
            # Vertex AI client for generative models (e.g., gemini-pro)
            cls._vertex_ai_prediction_client = aiplatform.PredictionServiceClient(client_options={
                "api_endpoint": f"{LOCATION}-aiplatform.googleapis.com"
            })
        return cls._vertex_ai_prediction_client

    @classmethod
    def get_translate_client(cls):
        if cls._translate_client is None:
            cls._translate_client = translate.TranslationServiceClient()
        return cls._translate_client

    @classmethod
    def get_firestore_client(cls):
        if cls._firestore_client is None:
            cls._firestore_client = firestore.Client(project=PROJECT_ID)
        return cls._firestore_client

    @classmethod
    def get_dlp_client(cls):
        if cls._dlp_client is None:
            cls._dlp_client = dlp.DlpServiceClient()
        return cls._dlp_client
