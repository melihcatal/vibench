import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult, DocumentContentFormat

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://YOUR_RESOURCE.cognitiveservices.azure.com/",
)

AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

DEFAULT_MODEL_ID = "prebuilt-layout"
DEFAULT_READ_MODEL_ID = "prebuilt-read"
DEFAULT_KEYVALUE_MODEL_ID = "prebuilt-document"


def get_document_intelligence_client(
    endpoint: str | None = None,
    key: str | None = None,
) -> DocumentIntelligenceClient:
    ep = endpoint or AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    api_key = key or AZURE_DOCUMENT_INTELLIGENCE_KEY
    credential = AzureKeyCredential(api_key)
    client = DocumentIntelligenceClient(
        endpoint=ep,
        credential=credential,
    )
    return client


def analyze_document(
    file_bytes: bytes,
    content_type: str = "application/pdf",
    model_id: str = DEFAULT_MODEL_ID,
    client: DocumentIntelligenceClient | None = None,
    **kwargs,
) -> AnalyzeResult:
    di_client = client or get_document_intelligence_client()
    poller = di_client.begin_analyze_document(
        model_id=model_id,
        analyze_request=file_bytes,
        content_type=content_type,
        **kwargs,
    )
    result = poller.result()
    return result


def analyze_document_from_url(
    file_url: str,
    model_id: str = DEFAULT_MODEL_ID,
    client: DocumentIntelligenceClient | None = None,
    **kwargs,
) -> AnalyzeResult:
    di_client = client or get_document_intelligence_client()
    poller = di_client.begin_analyze_document_from_url(
        model_id=model_id,
        analyze_request={"urlSource": file_url},
        **kwargs,
    )
    result = poller.result()
    return result


def build_content_type_from_path(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    mapping = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
        ".bmp": "image/bmp",
        ".heif": "image/heif",
    }
    return mapping.get(ext, "application/octet-stream")
