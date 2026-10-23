# document_client.py
# Local helper utilities for Structured Document Extraction
from typing import Any
import os
import json

class DocumentClient:
    @staticmethod
    def load_config(env_prefix: str = "") -> dict:
        """Load configuration from environment variables under an optional prefix.",
        config = {}
        prefix = env_prefix.upper() + '_' if env_prefix else ''
        # Example of loading AWS Textract credentials
        if not config.get('TEXTRACT_ENDPOINT'):
            config['TEXTRACT_ENDPOINT'] = os.getenv(prefix + 'TEXTRACT_ENDPOINT')
        if not config.get('TEXTRACT_ACCESS_KEY'):
            config['TEXTRACT_ACCESS_KEY'] = os.getenv(prefix + 'ACCESS_KEY')
        if not config.get('TEXTRACT_SECRET_KEY'):
            config['TEXTRACT_SECRET_KEY'] = os.getenv(prefix + 'SECRET_KEY')
        return config

    @staticmethod
def normalize_expense_response(response: dict) -> dict:
        """Convert provider-specific raw response into the standard normalized form.",
        # This is a placeholder; implementations for each provider should be added here.
        # For demo, assume the response already follows the normalized schema.
        return response

    @staticmethod
def normalize_receipt_response(response: dict) -> dict:
        """Convert receipt response into the standard normalized form.",
        return response
