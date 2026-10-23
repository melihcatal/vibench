import os
from typing import Optional
from alibabacloud_ocr_api20210707.models import RecognizeAdvancedRequest
from document_client import create_ocr_client, encode_image_to_base64
from document_models import (
    DocumentLayoutResult,
    OcrBlock,
    OcrLine,
    OcrWord,
    TableStructure,
    TableCell,
)


def extract_layout_from_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
) -> DocumentLayoutResult:
    client = create_ocr_client()
    image_base64 = encode_image_to_base64(image_path, image_bytes)

    request = RecognizeAdvancedRequest(body=image_base64)
    response = client.recognize_advanced(request)

    body = response.body
    blocks = []
    tables = []

    if hasattr(body, "data") and body.data:
        data = body.data
        if isinstance(data, dict):
            for block_data in data.get("blocks", []):
                block_type = block_data.get(
                    "type", block_data.get("block_type", "text")
                )
                lines = []
                for line_data in block_data.get("lines", []):
                    words = []
                    for word_data in line_data.get("words", []):
                        word = OcrWord(
                            text=word_data.get("text", ""),
                            confidence=word_data.get("confidence", 0.0),
                        )
                        words.append(word)
                    if words:
                        lines.append(OcrLine(words=words))
                blocks.append(
                    OcrBlock(
                        block_type=block_type,
                        lines=lines,
                    )
                )

            for table_data in data.get("tables", []):
                cells = []
                for cell_data in table_data.get("cells", []):
                    cell = TableCell(
                        row_index=cell_data.get("row", cell_data.get("row_index", 0)),
                        col_index=cell_data.get(
                            "column", cell_data.get("col_index", 0)
                        ),
                        text=cell_data.get("text", ""),
                        confidence=cell_data.get("confidence", 0.0),
                    )
                    cells.append(cell)
                tables.append(
                    TableStructure(
                        cells=cells,
                        num_rows=table_data.get(
                            "num_rows", len(set(c.row_index for c in cells))
                        ),
                        num_columns=table_data.get(
                            "num_columns", len(set(c.col_index for c in cells))
                        ),
                    )
                )

    return DocumentLayoutResult(blocks=blocks, tables=tables, page_count=1)


if __name__ == "__main__":
    image_file = os.environ.get("DOCUMENT_IMAGE_PATH")
    if image_file:
        result = extract_layout_from_image(image_path=image_file)
        for block in result.blocks:
            print(f"[{block.block_type}] {block.text}")
