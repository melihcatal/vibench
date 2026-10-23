from document_client import get_document_intelligence_client
from document_models import ExtractedLayout
import io


def extract_layout_from_document(document_content: bytes) -> ExtractedLayout:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        "prebuilt-layout", document_content, content_type="application/octet-stream"
    )
    result = poller.result()
    pages_data = []
    for page in result.pages:
        pages_data.append(
            {
                "page_number": page.page_number,
                "lines": [
                    {
                        "content": line.content,
                        "bounding_regions": [
                            r.to_dict() for r in line.bounding_regions
                        ],
                    }
                    for line in page.lines
                ],
            }
        )
    return ExtractedLayout(pages=pages_data)
