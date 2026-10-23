import os
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://your-resource.cognitiveservices.azure.com/",
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

AZURE_TRANSLATOR_ENDPOINT = os.getenv(
    "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com/"
)
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION", "global")

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://your-content-safety-resource.cognitiveservices.azure.com/",
)
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY", "")


def get_document_analysis_client():
    credential = AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY)
    client = DocumentAnalysisClient(
        endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, credential=credential
    )
    return client


def get_azure_translator_headers():
    return {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-Type": "application/json",
    }


def get_content_safety_credential():
    return AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY)


def load_image_bytes(image_path):
    with open(image_path, "rb") as f:
        return f.read()


def load_image_from_url(image_url):
    import urllib.request

    with urllib.request.urlopen(image_url) as response:
        return response.read()
