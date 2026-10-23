import os

# Document AI client configuration and helper utilities


def get_service_endpoint(service_name: str) -> str:
    """Return the base endpoint URL for the given OCR/Layout service.
    Supports:
    - azure-document-intelligence
    - google-document-ai
    - mindee
    - amazon-textract
    - alibaba-ocr
    """
    mapping = {
        "azure-document-intelligence": os.getenv(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"
        ),
        "google-document-ai": "https://documentai.googleapis.com/v1/",
        "mindee": "https://api.mined.ai/v1/",
        "amazon-textract": "https://textract.us-west-2.amazonaws.com/",
        "alibaba-ocr": "https://vision.cn-shanghai.aliyuncs.com/ocr/",
    }
    return mapping.get(service_name.lower())


def get_service_auth_headers(service_name: str, **extra_headers) -> dict:
    """Return authentication headers for the given service.
    Fills in common auth values from environment variables.
    """
    headers = extra_headers.copy()
    if service_name.lower() == "azure-document-intelligence":
        headers.update(
            {
                "Ocp-Apim-Subscription-Key": os.getenv(
                    "AZURE_DOCUMENT_INTELLIGENCE_KEY"
                ),
            }
        )
    elif service_name.lower() == "google-document-ai":
        # Use Application Default Credentials, no header needed here
        pass
    elif service_name.lower() == "mindee":
        headers.update({"Authorization": f"Bearer {os.getenv('MINDEE_API_KEY')}"})
    elif service_name.lower() == "amazon-textract":
        # boto3 client handles auth via environment variables
        pass
    elif service_name.lower() == "alibaba-ocr":
        headers.update(
            {
                "Authorization": os.getenv("ALIBABA_CLOUD_ACCESS_TOKEN"),
                "x-acs-signature": os.getenv("ALIBABA_CLOUD_ACCESS_TOKEN"),
            }
        )
    else:
        raise ValueError(f"Unsupported OCR/Layout service: {service_name}")
    return headers
