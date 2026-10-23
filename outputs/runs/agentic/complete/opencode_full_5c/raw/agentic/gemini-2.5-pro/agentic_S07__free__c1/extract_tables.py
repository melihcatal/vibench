from typing import List
from document_client import get_document_intelligence_client
from document_models import Table, TableCell, BoundingRegion, Point, Span


def extract_tables(image_path: str) -> List[Table]:
    """
    Extracts tables from a document image.
    """
    client = get_document_intelligence_client()

    with open(image_path, "rb") as f:
        poller = client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream",
        )
    result = poller.result()

    extracted_tables = []
    if result.tables:
        for table in result.tables:
            cells = []
            for cell in table.cells:
                regions = []
                if cell.bounding_regions:
                    for region in cell.bounding_regions:
                        points = [Point(x=p.x, y=p.y) for p in region.polygon]
                        regions.append(
                            BoundingRegion(
                                page_number=region.page_number, polygon=points
                            )
                        )

                spans = [Span(offset=s.offset, length=s.length) for s in cell.spans]

                cells.append(
                    TableCell(
                        kind=cell.kind,
                        content=cell.content,
                        bounding_regions=regions,
                        spans=spans,
                        row_index=cell.row_index,
                        column_index=cell.column_index,
                        row_span=cell.row_span or 1,
                        column_span=cell.column_span or 1,
                    )
                )

            table_regions = []
            if table.bounding_regions:
                for region in table.bounding_regions:
                    points = [Point(x=p.x, y=p.y) for p in region.polygon]
                    table_regions.append(
                        BoundingRegion(page_number=region.page_number, polygon=points)
                    )

            extracted_tables.append(
                Table(
                    row_count=table.row_count,
                    column_count=table.column_count,
                    cells=cells,
                    bounding_regions=table_regions,
                    spans=[Span(offset=s.offset, length=s.length) for s in table.spans],
                )
            )

    return extracted_tables
