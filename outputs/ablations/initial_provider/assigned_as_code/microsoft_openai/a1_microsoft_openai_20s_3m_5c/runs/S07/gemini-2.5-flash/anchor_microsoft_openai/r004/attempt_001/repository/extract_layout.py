import io
from document_client import get_document_intelligence_client
from document_models import DocumentAnalysisResponse

def extract_layout(payload):
    client = get_document_intelligence_client()
    with client:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            body=io.BytesIO(payload['document_bytes']), 
            content_type=payload['mime_type']
        )
        result = poller.result()

    pages_data = []
    for page in result.pages:
        pages_data.append({
            "page_number": page.page_number,
            "width": page.width,
            "height": page.height,
            "unit": page.unit,
            "lines": [{"content": line.content, "bounding_regions": [br.as_dict() for br in line.bounding_regions]} for line in page.lines]
        })

    return DocumentAnalysisResponse(content=result.content, pages=pages_data)._asdict()
