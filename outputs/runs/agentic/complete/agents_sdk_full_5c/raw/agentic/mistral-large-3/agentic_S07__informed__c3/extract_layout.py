from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential
import os

from document_client import get_document_intelligence_client
from document_models import LayoutResponse


def extract_layout_from_image(image_path: str) -> LayoutResponse:
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read())
        )

    result: AnalyzeResult = poller.result()

    return LayoutResponse(
        paragraphs=[
            {
                "content": paragraph.content,
                "bounding_box": paragraph.polygon,
                "role": paragraph.role
            }
            for paragraph in result.paragraphs
        ],
        tables=[
            {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "bounding_box": table.bounding_regions[0].polygon if table.bounding_regions else None,
                "cells": [
                    {
                        "content": cell.content,
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                        "bounding_box": cell.bounding_regions[0].polygon if cell.bounding_regions else None
                    }
                    for cell in table.cells
                ]
            }
            for table in result.tables
        ],
        sections=[
            {
                "content": section.content,
                "bounding_box": section.bounding_regions[0].polygon if section.bounding_regions else None
            }
            for section in result.sections
        ]
    )