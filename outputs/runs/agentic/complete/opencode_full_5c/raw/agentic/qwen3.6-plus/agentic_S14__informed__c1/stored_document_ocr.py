import json

from storage_client import (
    get_s3_client,
    get_textract_client,
    validate_bucket_name,
    validate_object_key,
)
from storage_models import OcrRequest, OcrResponse, OcrPage


def run_ocr_on_stored_document(
    bucket: str,
    key: str,
    version_id: str = None,
    pages: list = None,
) -> OcrResponse:
    s3_client = get_s3_client()
    textract_client = get_textract_client()
    validate_bucket_name(bucket)
    validate_object_key(key)

    try:
        s3_object = {"S3Object": {"Bucket": bucket, "Name": key}}
        if version_id:
            s3_object["S3Object"]["Version"] = version_id

        textract_params = {
            "Document": s3_object,
        }

        if pages:
            textract_params["Page"] = pages

        response = textract_client.detect_document_text(**textract_params)

        ocr_pages = []
        all_text_blocks = []
        current_page = 1
        page_text = []
        page_blocks = []

        for block in response.get("Blocks", []):
            block_type = block.get("BlockType")

            if block_type == "PAGE":
                if page_text:
                    ocr_pages.append(
                        OcrPage(
                            page_number=current_page,
                            text="\n".join(page_text),
                            confidence=_compute_page_confidence(page_blocks),
                            blocks=page_blocks,
                        )
                    )
                    all_text_blocks.extend(page_blocks)
                current_page = block.get("Page", current_page)
                page_text = []
                page_blocks = []
                continue

            if block_type in ("LINE", "WORD"):
                text = block.get("Text", "")
                confidence = block.get("Confidence", 0.0)
                if text.strip():
                    page_text.append(text)
                page_blocks.append(
                    {
                        "type": block_type,
                        "text": text,
                        "confidence": confidence,
                        "id": block.get("Id"),
                        "geometry": block.get("Geometry"),
                    }
                )

        if page_text:
            ocr_pages.append(
                OcrPage(
                    page_number=current_page,
                    text="\n".join(page_text),
                    confidence=_compute_page_confidence(page_blocks),
                    blocks=page_blocks,
                )
            )
            all_text_blocks.extend(page_blocks)

        full_text = "\n\n".join(p.text for p in ocr_pages)
        avg_confidence = _compute_page_confidence(all_text_blocks)

        return OcrResponse(
            success=True,
            document_key=key,
            pages=ocr_pages,
            full_text=full_text,
            average_confidence=avg_confidence,
        )

    except Exception as exc:
        return OcrResponse(
            success=False,
            document_key=key,
            error=str(exc),
        )


def _compute_page_confidence(blocks):
    if not blocks:
        return 0.0
    confidences = [b.get("confidence", 0.0) for b in blocks if b.get("confidence")]
    if not confidences:
        return 0.0
    return sum(confidences) / len(confidences)


def run_ocr_from_request(request: OcrRequest) -> OcrResponse:
    return run_ocr_on_stored_document(
        bucket=request.bucket,
        key=request.key,
        version_id=request.version_id,
        pages=request.pages,
    )
