from typing import List, Dict, Any
from document_client import get_comprehend_client
from document_models import DocumentFieldExtractionRequest, DocumentFieldExtractionResponse
import os

def extract_document_fields(request: DocumentFieldExtractionRequest) -> DocumentFieldExtractionResponse:
    comprehend_client = get_comprehend_client()

    # For structured field extraction, AWS Comprehend's Custom Entity Recognition (CER) is the most suitable.
    # This would typically involve a custom-trained model. For demonstration purposes, we will call
    # detect_entities and assume a custom endpoint if CUSTOM_COMPREHEND_ENDPOINT is set.
    # In a real-world scenario, you would provide a pre-trained custom entity recognizer ARN.

    # Example: Using a custom endpoint if available, otherwise default entity detection
    # Note: A real custom entity recognizer requires training and an endpoint ARN.
    # For this exercise, we simulate by checking for an environment variable.
    custom_comprehend_endpoint = os.getenv('CUSTOM_COMPREHEND_ENDPOINT_ARN')

    if custom_comprehend_endpoint:
        # This is a placeholder call. A real custom entity recognition call might look different
        # and require a specific model ARN rather than an endpoint URL in detect_entities.
        # The detect_entities API itself is for built-in entities unless a specific PII/custom entity API is used.
        # For custom entities, the client.detect_custom_entities API is used, which requires a model ARN.
        # Given the constraint to use `comprehend_client.detect_entities` for simplicity in this example,
        # we'll just demonstrate general entity detection.
        response = comprehend_client.detect_entities(
            Text=request.text,
            LanguageCode=request.language_code
        )
    else:
        response = comprehend_client.detect_entities(
            Text=request.text,
            LanguageCode=request.language_code
        )

    extracted_fields = response['Entities']

    return DocumentFieldExtractionResponse(
        extracted_fields=extracted_fields
    )
