from typing import List, Dict, Optional
from dataclasses import dataclass
from google.cloud import vision_v1
from google.cloud.vision_v1 import types


@dataclass
class OCRResponse:
    text: str
    language: Optional[str] = None

    @classmethod
    def from_vision_response(
        cls, response: types.AnnotateImageResponse
    ) -> "OCRResponse":
        return cls(text=response.full_text_annotation.text)


@dataclass
class BoundingPoly:
    vertices: List[Dict[str, int]]

    @classmethod
    def from_vision_bounding_poly(cls, poly: types.BoundingPoly) -> "BoundingPoly":
        return cls(vertices=[{"x": v.x, "y": v.y} for v in poly.vertices])


@dataclass
class LayoutBlock:
    text: str
    bounding_box: BoundingPoly
    block_type: str

    @classmethod
    def from_vision_block(cls, block: types.Block) -> "LayoutBlock":
        return cls(
            text="".join(
                [
                    symbol.text
                    for paragraph in block.paragraphs
                    for word in paragraph.words
                    for symbol in word.symbols
                ]
            ),
            bounding_box=BoundingPoly.from_vision_bounding_poly(block.bounding_box),
            block_type=types.Block.BlockType(block.block_type).name,
        )


@dataclass
class LayoutResponse:
    blocks: List[LayoutBlock]


@dataclass
class TableCell:
    text: str
    row_span: int
    col_span: int
    bounding_box: BoundingPoly

    @classmethod
    def from_vision_cell(cls, cell: types.TableCell) -> "TableCell":
        return cls(
            text="".join(
                [symbol.text for symbol in cell.layout.text_annotation.symbols]
            ),
            row_span=cell.row_span,
            col_span=cell.col_span,
            bounding_box=BoundingPoly.from_vision_bounding_poly(
                cell.layout.bounding_poly
            ),
        )


@dataclass
class TableRow:
    cells: List[TableCell]

    @classmethod
    def from_vision_row(cls, row: types.TableRow) -> "TableRow":
        return cls(cells=[TableCell.from_vision_cell(cell) for cell in row.cells])


@dataclass
class Table:
    rows: List[TableRow]
    header_rows: List[TableRow]
    bounding_box: BoundingPoly

    @classmethod
    def from_vision_table(cls, table: types.Table) -> "Table":
        return cls(
            rows=[TableRow.from_vision_row(row) for row in table.body_rows],
            header_rows=[TableRow.from_vision_row(row) for row in table.header_rows],
            bounding_box=BoundingPoly.from_vision_bounding_poly(table.bounding_box),
        )


@dataclass
class TableResponse:
    tables: List[Table]


@dataclass
class KeyValuePair:
    key: str
    value: str


@dataclass
class KeyValueResponse:
    pairs: List[KeyValuePair]
