import os
from typing import Any, Dict, Optional

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from storage_client import get_bucket_name, get_s3_client
from storage_models import normalize_key


def run_stored_document_ocr(bucket: Optional[str], key: str) -> Dict[str, Any]:
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=get_bucket_name(bucket), Key=normalize_key(key))
    document_bytes = obj["Body"].read()
    client = DocumentIntelligenceClient(
        endpoint=os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
        credential=AzureKeyCredential(os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]),
    )
    poller = client.begin_analyze_document("prebuilt-read", body=document_bytes)
    result = poller.result()
    return {"pages": len(result.pages or []), "content": result.content}
