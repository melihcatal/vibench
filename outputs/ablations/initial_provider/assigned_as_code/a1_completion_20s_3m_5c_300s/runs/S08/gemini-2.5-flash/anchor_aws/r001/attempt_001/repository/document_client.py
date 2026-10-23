import os
from typing import Dict, Any
import boto3
from google.cloud import documentai_v1 as documentai

def get_aws_client(service_name: str, region_name: str) -> Any:
    """Provides an AWS client for the specified service."""
    return boto3.client(service_name, region_name=region_name)

def get_google_document_ai_client() -> documentai.DocumentProcessorServiceClient:
    """Provides a Google Cloud Document AI client."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    return documentai.DocumentProcessorServiceClient()

def load_config() -> Dict[str, Any]:
    """Loads configuration from environment variables."""
    config = {
        "aws_region": os.environ.get("AWS_REGION", "us-east-1"),
        "google_project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
        "google_location": os.environ.get("GOOGLE_CLOUD_LOCATION", "us"),
        "google_document_ai_processor_id_receipt": os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID_RECEIPT"),
        "google_document_ai_processor_id_invoice": os.environ.get("GOOGLE_DOCUMENT_AI_PROCESSOR_ID_INVOICE"),
        "google_generative_model_name": os.environ.get("GOOGLE_GENERATIVE_MODEL_NAME", "gemini-pro"),
        "google_translate_location": os.environ.get("GOOGLE_TRANSLATE_LOCATION", "global"),
        "google_firestore_collection": os.environ.get("GOOGLE_FIRESTORE_COLLECTION", "expense_records"),
        "aws_comprehend_language_code": os.environ.get("AWS_COMPREHEND_LANGUAGE_CODE", "en"),
        "aws_comprehend_entity_recognizer_arn": os.environ.get("AWS_COMPREHEND_ENTITY_RECOGNIZER_ARN"),
        "aws_s3_bucket": os.environ.get("AWS_S3_BUCKET"), # For potentially storing documents before processing
    }
    return config
