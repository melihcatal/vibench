import os
import base64
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from storage_client import get_oss_bucket, normalize_object_key


def run_ocr_on_stored_document(
    bucket_name: str,
    object_key: str,
    model_id: str = "prebuilt-read",
    language: str = "en",
) -> dict:
    object_key = normalize_object_key(object_key)
    bucket = get_oss_bucket(bucket_name)

    object_stream = bucket.get_object(object_key)
    document_bytes = object_stream.read()

    endpoint = os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        "https://<your-resource>.cognitiveservices.azure.com/",
    )
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

    credential = AzureKeyCredential(key)
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=credential)

    poller = client.begin_analyze_document(
        model_id=model_id,
        body=document_bytes,
        content_type="application/octet-stream",
    )
    result: AnalyzeResult = poller.result()

    pages_text = []
    if result.pages:
        for page in result.pages:
            page_text = ""
            if page.lines:
                for line in page.lines:
                    page_text += line.content + "\n"
            pages_text.append(page_text.strip())

    full_text = result.content or ""
    tables_data = []
    if result.tables:
        for table in result.tables:
            cells = []
            if table.cells:
                for cell in table.cells:
                    cells.append(
                        {
                            "row_index": cell.row_index,
                            "column_index": cell.column_index,
                            "content": cell.content,
                        }
                    )
            tables_data.append(
                {
                    "row_count": table.row_count,
                    "column_count": table.column_count,
                    "cells": cells,
                }
            )

    return {
        "success": True,
        "object_key": object_key,
        "bucket": bucket_name,
        "model_id": model_id,
        "full_text": full_text,
        "pages_text": pages_text,
        "tables": tables_data,
        "page_count": len(result.pages) if result.pages else 0,
    }
