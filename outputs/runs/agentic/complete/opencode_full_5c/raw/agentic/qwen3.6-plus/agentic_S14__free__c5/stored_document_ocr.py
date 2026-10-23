import json
from typing import Optional

from botocore.exceptions import ClientError

from storage_client import (
    get_s3_client,
    get_textract_client,
    read_object_content,
    handle_aws_error,
)
from storage_models import StorageConfig, OcrRequest, OcrResponse


def run_ocr_on_stored_document(
    bucket: str,
    key: str,
    version_id: Optional[str] = None,
    detect_tables: bool = True,
    detect_forms: bool = False,
    pages: Optional[list] = None,
    config: Optional[StorageConfig] = None,
) -> OcrResponse:
    s3_client = get_s3_client(config)
    textract_client = get_textract_client(config)

    try:
        document_bytes = read_object_content(s3_client, bucket, key, version_id)

        textract_kwargs = {"Document": {"Bytes": document_bytes}}

        features = ["TABLES"] if detect_tables else []
        if detect_forms:
            features.append("FORMS")

        if features:
            textract_kwargs["FeatureTypes"] = features

        if pages:
            textract_kwargs["Page"] = pages

        response = textract_client.analyze_document(**textract_kwargs)

        full_text = []
        page_results = []
        table_results = []
        total_confidence = 0.0
        block_count = 0

        for block in response.get("Blocks", []):
            block_type = block.get("BlockType")
            confidence = block.get("Confidence", 0.0)

            if block_type == "LINE":
                text = block.get("Text", "")
                full_text.append(text)
                total_confidence += confidence
                block_count += 1

            if block_type == "PAGE":
                page_results.append(
                    {
                        "page_num": block.get("Page"),
                        "width": block.get("Geometry", {})
                        .get("BoundingBox", {})
                        .get("Width", 0),
                        "height": block.get("Geometry", {})
                        .get("BoundingBox", {})
                        .get("Height", 0),
                        "confidence": confidence,
                    }
                )

            if block_type == "TABLE":
                table_results.append(
                    {
                        "table_id": block.get("Id"),
                        "row_count": block.get("RowCount", 0),
                        "column_count": block.get("ColumnCount", 0),
                        "confidence": confidence,
                    }
                )

        avg_confidence = total_confidence / block_count if block_count > 0 else 0.0

        return OcrResponse(
            success=True,
            text="\n".join(full_text),
            pages=page_results,
            tables=table_results,
            confidence=round(avg_confidence, 4),
        )

    except ClientError as e:
        return OcrResponse(
            success=False,
            error=handle_aws_error(e, "run_ocr_on_stored_document"),
        )
    except Exception as e:
        return OcrResponse(
            success=False,
            error=f"run_ocr_on_stored_document error: {str(e)}",
        )


def run_ocr_from_request(
    request: OcrRequest,
    config: Optional[StorageConfig] = None,
) -> OcrResponse:
    return run_ocr_on_stored_document(
        bucket=request.bucket,
        key=request.key,
        version_id=request.version_id,
        detect_tables=request.detect_tables,
        detect_forms=request.detect_forms,
        pages=request.pages,
        config=config,
    )
