import dataclasses
from typing import List, Dict, Any


@dataclasses.dataclass
class TextSegment:
    start_index: str
    end_index: str
    text_content: str


@dataclasses.dataclass
class TextAnchor:
    text_segments: List[TextSegment]


@dataclasses.dataclass
class Layout:
    text_anchor: TextAnchor
    bounding_poly: Dict[str, Any]


@dataclasses.dataclass
class Cell:
    layout: Layout
    row_span: int
    col_span: int


@dataclasses.dataclass
class Row:
    cells: List[Cell]


@dataclasses.dataclass
class Table:
    header_rows: List[Row]
    body_rows: List[Row]


@dataclasses.dataclass
class Page:
    page_number: int
    tables: List[Table]
    text: str
    # Add other page-level elements as needed


@dataclasses.dataclass
class Document:
    text: str
    pages: List[Page]
    entities: List[Dict[str, Any]]  # Simplified for now

    @classmethod
    def from_documentai_document(cls, doc_ai_document):
        pages = []
        for page_ai in doc_ai_document.pages:
            tables = []
            for table_ai in page_ai.tables:
                header_rows = []
                for row_ai in table_ai.header_rows:
                    cells = []
                    for cell_ai in row_ai.cells:
                        text_segments = [
                            TextSegment(ts.start_index, ts.end_index, ts.text_content)
                            for ts in cell_ai.layout.text_anchor.text_segments
                        ]
                        text_anchor = TextAnchor(text_segments)
                        layout = Layout(
                            text_anchor, {}
                        )  # bounding_poly is complex, simplifying
                        cells.append(Cell(layout, cell_ai.row_span, cell_ai.col_span))
                    header_rows.append(Row(cells))

                body_rows = []
                for row_ai in table_ai.body_rows:
                    cells = []
                    for cell_ai in row_ai.cells:
                        text_segments = [
                            TextSegment(ts.start_index, ts.end_index, ts.text_content)
                            for ts in cell_ai.layout.text_anchor.text_segments
                        ]
                        text_anchor = TextAnchor(text_segments)
                        layout = Layout(text_anchor, {})
                        cells.append(Cell(layout, cell_ai.row_span, cell_ai.col_span))
                    body_rows.append(Row(cells))
                tables.append(Table(header_rows, body_rows))

            pages.append(Page(page_ai.page_number, tables, page_ai.text))

        entities = []
        for entity_ai in doc_ai_document.entities:
            entity_dict = {
                "type_": entity_ai.type_,
                "mention_text": entity_ai.mention_text,
                "normalized_value": entity_ai.normalized_value.text
                if entity_ai.normalized_value
                else None,
            }
            entities.append(entity_dict)

        return cls(text=doc_ai_document.text, pages=pages, entities=entities)
