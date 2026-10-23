import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from document_models import LayoutElement
from document_client import load_document_image
from typing import List, Dict, Any

def extract_layout(image_path: str) -> List[LayoutElement]:
    """
    Extract layout elements (lines, paragraphs, etc.) using Azure AI Document Intelligence prebuilt-layout.
    """
    endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    poller = client.begin_analyze_document("prebuilt-layout", load_document_image(image_path))
    result: AnalyzeResult = poller.result()

    layout: List[LayoutElement] = []
    for page in result.pages or []:
        if hasattr(page, 'lines') and page.lines:
            for line in page.lines:
                bbox = [p.offset for p in (line.polygon or [])]
                layout.append({
                    'type': 'line',
                    'text': line.content,
                    'confidence': getattr(line, 'confidence', None),
                    'bbox': bbox
                })
        if hasattr(page, 'paragraphs') and page.paragraphs:
            for para in page.paragraphs:
                bbox = [p.offset for p in (para.polygon or [])]
                layout.append({
                    'type': 'paragraph',
                    'text': para.content,
                    'confidence': getattr(para, 'confidence', None),
                    'bbox': bbox
                })
    return layout
