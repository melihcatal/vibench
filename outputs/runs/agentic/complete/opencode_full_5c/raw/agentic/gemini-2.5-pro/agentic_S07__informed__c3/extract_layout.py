from typing import List
from document_client import get_document_analysis_client
from document_models import DocumentLayout, BoundingBox


def extract_layout_from_document(
    file_path: str = None, url: str = None
) -> List[DocumentLayout]:
    client = get_document_analysis_client()

    poller = None
    if url:
        poller = client.begin_analyze_document("prebuilt-layout", {"urlSource": url})
    elif file_path:
        with open(file_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-layout", f.read())
    else:
        raise ValueError("Either file_path or url must be provided.")

    result = poller.result()

    layouts = []
    if result.paragraphs:
        for paragraph in result.paragraphs:
            bounding_regions = []
            if paragraph.bounding_regions:
                bounding_regions = [
                    BoundingBox(polygon=region.polygon)
                    for region in paragraph.bounding_regions
                ]

            layouts.append(
                DocumentLayout(
                    bounding_box=bounding_regions[0]
                    if bounding_regions
                    else BoundingBox(polygon=[]),
                    content=paragraph.content,
                )
            )

    return layouts
