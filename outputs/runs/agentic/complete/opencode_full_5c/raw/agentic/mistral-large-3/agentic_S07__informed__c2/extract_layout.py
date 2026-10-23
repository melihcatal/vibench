from typing import Dict, List, Optional
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import (
    AnalyzeDocumentRequest,
    AnalyzeResult,
    DocumentPage,
    DocumentLine,
    DocumentWord,
    DocumentTable,
    DocumentFigure,
)
from azure.core.credentials import AzureKeyCredential


def extract_layout(image_path: str) -> Dict:
    """
    Extracts layout elements (blocks, lines, tables, figures) from a document using Azure Document Intelligence.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured.")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=AnalyzeDocumentRequest(bytes_source=f.read()),
        )

    result: AnalyzeResult = poller.result()

    layout_data = {"pages": [], "lines": [], "tables": [], "figures": []}

    if result.pages:
        for page in result.pages:
            page_data = {
                "page_number": page.page_number,
                "width": page.width,
                "height": page.height,
                "angle": page.angle,
                "unit": page.unit,
            }
            layout_data["pages"].append(page_data)

    if result.tables:
        for table in result.tables:
            table_data = {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": [],
            }
            for cell in table.cells:
                cell_data = {
                    "row_index": cell.row_index,
                    "column_index": cell.column_index,
                    "content": cell.content,
                    "bounding_box": [
                        {"x": point.x, "y": point.y}
                        for point in cell.bounding_regions[0].polygon
                    ]
                    if cell.bounding_regions
                    else [],
                }
                table_data["cells"].append(cell_data)
            layout_data["tables"].append(table_data)

    if result.paragraphs:
        for paragraph in result.paragraphs:
            for line in paragraph.spans:
                layout_data["lines"].append(
                    {
                        "content": paragraph.content,
                        "bounding_box": [
                            {"x": point.x, "y": point.y} for point in line.polygon
                        ]
                        if hasattr(line, "polygon")
                        else [],
                    }
                )

    if result.figures:
        for figure in result.figures:
            figure_data = {
                "content": figure.content,
                "bounding_box": [
                    {"x": point.x, "y": point.y}
                    for point in figure.bounding_regions[0].polygon
                ]
                if figure.bounding_regions
                else [],
            }
            layout_data["figures"].append(figure_data)

    return layout_data
