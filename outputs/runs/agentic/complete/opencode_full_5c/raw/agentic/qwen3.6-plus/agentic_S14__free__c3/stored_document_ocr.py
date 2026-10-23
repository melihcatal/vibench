from storage_client import get_textract_client, validate_bucket_name
from storage_models import OcrRequest, OcrResponse, OcrPage


def run_ocr_on_stored_document(request: OcrRequest) -> OcrResponse:
    textract_client = get_textract_client()
    validate_bucket_name(request.bucket)

    document = {
        "S3Object": {
            "Bucket": request.bucket,
            "Name": request.key,
        }
    }

    if request.version_id:
        document["S3Object"]["Version"] = request.version_id

    try:
        response = textract_client.detect_document_text(Document=document)

        pages = []
        full_text_lines = []

        current_page_blocks = []
        current_page_text = []

        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                text = block.get("Text", "")
                current_page_text.append(text)
                current_page_blocks.append(block)
            elif block["BlockType"] == "PAGE":
                if current_page_text:
                    pages.append(
                        OcrPage(
                            page_number=len(pages) + 1,
                            text="\n".join(current_page_text),
                            blocks=current_page_blocks,
                        )
                    )
                    full_text_lines.extend(current_page_text)
                    current_page_text = []
                    current_page_blocks = []

        if current_page_text:
            pages.append(
                OcrPage(
                    page_number=len(pages) + 1,
                    text="\n".join(current_page_text),
                    blocks=current_page_blocks,
                )
            )
            full_text_lines.extend(current_page_text)

        full_text = "\n".join(full_text_lines)

        return OcrResponse(
            success=True,
            pages=pages,
            full_text=full_text,
        )
    except Exception as e:
        error_msg = str(e)
        if "AccessDenied" in error_msg:
            error_msg = f"Amazon Textract access denied for s3://{request.bucket}/{request.key}. Check IAM permissions."
        elif "InvalidS3Object" in error_msg:
            error_msg = f"Amazon Textract could not read s3://{request.bucket}/{request.key}. Verify the object exists and is a supported format (PNG, JPEG, PDF, TIFF)."
        return OcrResponse(
            success=False,
            error=error_msg,
        )
