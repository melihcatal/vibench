import os
from typing import BinaryIO
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from document_models import LayoutResponse, LayoutBlock

def extract_layout(image_data: BinaryIO) -> LayoutResponse:
    """Extract layout elements (blocks, lines, tables) from a document using Azure Form Recognizer."""
    endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
    key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
    
    if not endpoint or not key:
        raise ValueError("Azure Form Recognizer credentials not configured.")
    
    client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = client.begin_analyze_document("prebuilt-layout", document=image_data.read())
    result = poller.result()
    
    blocks = []
    for paragraph in result.paragraphs:
        blocks.append(LayoutBlock(
            block_type="paragraph",
            text=paragraph.content,
            bounding_box=paragraph.bounding_regions[0].polygon
        ))
    
    for table in result.tables:
        blocks.append(LayoutBlock(
            block_type="table",
            text=f"Table with {table.row_count} rows and {table.column_count} columns",
            bounding_box=table.bounding_regions[0].polygon
        ))
    
    return LayoutResponse(blocks=blocks)