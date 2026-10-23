import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import document_client

def extract_layout(image_path: str) -> list[dict]:
    endpoint = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
    key = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    image_bytes = document_client.load_image(image_path)
    content_type = document_client.get_mimetype(image_path)
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        document=image_bytes,
        content_type=content_type
    )
    result = poller.result()
    layout_elements = []
    for paragraph in result.paragraphs or []:
        element = {'type': 'paragraph', 'content': paragraph.content}
        if paragraph.bounding_regions:
            element['bbox'] = [polygon.x + polygon.y * 1j for polygon in paragraph.bounding_regions[0].polygon]
        layout_elements.append(element)
    for table in result.tables or []:
        layout_elements.append({'type': 'table', 'row_count': table.row_count, 'column_count': table.column_count})
    return layout_elements
