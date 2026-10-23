import os
from typing import Any, Dict

# Provider – example: AWS Textract (or Azure, Google, etc.)
TEXTRACT_ENDPOINT = os.getenv("TEXTRACT_ENDPOINT")
TEXTRACT_ACCESS_KEY = os.getenv("TEXTRACT_ACCESS_KEY")
TEXTRACT_SECRET_KEY = os.getenv("TEXTRACT_SECRET_KEY")


class DocumentClient:
    """Thin wrapper that abstracts provider-specific calls for structured document extraction.","""

    def __init__(self):
        # In a real implementation you would initialize an SDK client here, e.g. boto3.client('textract')
        pass

    def extract_document(
        self, document_bytes: bytes, document_type: str
    ) -> Dict[str, Any]:
        """Return raw fields extracted by the provider.","""
        # Placeholder for provider request – replace with real SDK call or HTTP request
        # Example for AWS Textract AnalyzeExpense
        # response = textract_client.analyze_expense( Bytes=document_bytes )
        # For demo we return a dummy payload
        if document_type.lower() == "invoice":
            return {
                "vendor": "Acme Co.",
                "date": "2024-07-01",
                "total": 210.75,
                "items": [
                    {
                        "description": "Office Supplies",
                        "quantity": 3,
                        "unitPrice": 10.0,
                        "tax": 0.07,
                    },
                    {
                        "description": "Furniture",
                        "quantity": 1,
                        "unitPrice": 95.5,
                        "tax": 0.07,
                    },
                ],
            }
        elif document_type.lower() == "receipt":
            return {
                "merchant": "Joe's Cafe",
                "date": "2024-07-02",
                "total": 18.90,
                "items": [
                    {"name": "Coffee", "quantity": 2, "price": 1.5, "tax": 0.05},
                    {"name": "Sandwich", "quantity": 1, "price": 10.0, "tax": 0.05},
                ],
            }
        raise ValueError("Unsupported document type")
