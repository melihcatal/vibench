import os
from typing import Optional, List, Dict, Any
from storage_client import get_s3_client, get_textract_client, get_object_bytes
from storage_models import OCRRequest, OCRResponse, OCRPage


def run_ocr_on_stored_document(request: OCRRequest) -> OCRResponse:
    s3_client = get_s3_client()
    textract_client = get_textract_client(region=request.region)

    try:
        document_bytes = get_object_bytes(
            s3_client, request.bucket, request.key, request.version_id
        )
    except Exception as e:
        return OCRResponse(
            success=False,
            document_key=request.key,
            error_message=f"Failed to retrieve object from S3: {str(e)}",
        )

    try:
        detect_args: Dict[str, Any] = {
            "Document": {"Bytes": document_bytes},
        }

        if request.detect_tables:
            detect_args["FeatureTypes"] = ["TABLES"]
            if request.detect_forms:
                detect_args["FeatureTypes"].append("FORMS")
        elif request.detect_forms:
            detect_args["FeatureTypes"] = ["FORMS"]

        response = textract_client.detect_document_text(**detect_args)

        pages: List[OCRPage] = []
        full_text_parts: List[str] = []
        tables: List[List[List[str]]] = []

        blocks = response.get("Blocks", [])

        page_blocks: Dict[int, List[Dict[str, Any]]] = {}
        for block in blocks:
            if block["BlockType"] == "PAGE":
                page_num = block.get("Page", 1)
                if page_num not in page_blocks:
                    page_blocks[page_num] = []
                page_blocks[page_num].append(block)

        for block in blocks:
            if block["BlockType"] in ("LINE", "WORD"):
                page_num = block.get("Page", 1)
                if page_num not in page_blocks:
                    page_blocks[page_num] = []
                page_blocks[page_num].append(block)

        for page_num in sorted(page_blocks.keys()):
            p_blocks = page_blocks[page_num]
            page_lines = [b for b in p_blocks if b["BlockType"] == "LINE"]
            page_text = "\n".join(line.get("Text", "") for line in page_lines)
            full_text_parts.append(page_text)

            avg_confidence = 0.0
            if page_lines:
                confidences = [line.get("Confidence", 0) for line in page_lines]
                avg_confidence = sum(confidences) / len(confidences)

            pages.append(
                OCRPage(
                    page_number=page_num,
                    text=page_text,
                    confidence=avg_confidence,
                    blocks=p_blocks,
                )
            )

        table_blocks = [b for b in blocks if b["BlockType"] == "TABLE"]
        for table_block in table_blocks:
            table_page = table_block.get("Page", 1)
            cell_blocks = [
                b
                for b in blocks
                if b["BlockType"] == "CELL" and b.get("Page") == table_page
            ]
            row_indices = set()
            col_indices = set()
            cell_map: Dict[tuple, str] = {}

            for cell in cell_blocks:
                row_idx = cell.get("RowIndex", 0)
                col_idx = cell.get("ColumnIndex", 0)
                row_indices.add(row_idx)
                col_indices.add(col_idx)

                cell_text = ""
                if "Relationships" in cell:
                    for rel in cell["Relationships"]:
                        if rel["Type"] == "CHILD":
                            for child_id in rel["Ids"]:
                                child_block = next(
                                    (b for b in blocks if b["Id"] == child_id), None
                                )
                                if child_block and child_block["BlockType"] == "WORD":
                                    cell_text += child_block.get("Text", "") + " "
                cell_map[(row_idx, col_idx)] = cell_text.strip()

            max_row = max(row_indices) if row_indices else 0
            max_col = max(col_indices) if col_indices else 0

            table_data = []
            for r in range(1, max_row + 1):
                row_data = []
                for c in range(1, max_col + 1):
                    row_data.append(cell_map.get((r, c), ""))
                table_data.append(row_data)
            tables.append(table_data)

        full_text = "\n\n".join(full_text_parts)

        return OCRResponse(
            success=True,
            document_key=request.key,
            pages=pages,
            full_text=full_text,
            tables=tables,
        )
    except Exception as e:
        return OCRResponse(
            success=False,
            document_key=request.key,
            error_message=f"Textract OCR failed: {str(e)}",
        )


def ocr_stored_document(
    bucket: str, key: str, detect_tables: bool = True, region: Optional[str] = None
) -> OCRResponse:
    request = OCRRequest(
        bucket=bucket,
        key=key,
        detect_tables=detect_tables,
        region=region,
    )
    return run_ocr_on_stored_document(request)
