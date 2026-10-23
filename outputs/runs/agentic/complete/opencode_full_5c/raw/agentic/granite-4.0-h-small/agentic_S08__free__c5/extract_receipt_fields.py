# provider: AWS Textract

from boto3 import client as boto3_client
from document_models import ReceiptFieldsResponse

# Local helper import for configuration
from document_client import get_textract_credentials, get_textract_endpoint

SESSION = boto3_client(
    "textract",
    region_name=get_textract_credentials().get("region", "us-east-1"),
    aws_access_key_id=get_textract_credentials().get("access_key"),
    aws_secret_access_key=get_textract_credentials().get("secret_key"),
)

MODEL_ID = "receipt"


def extract_receipt_fields(file_path: str) -> ReceiptFieldsResponse:
    with open(file_path, "rb") as image_file:
        response = SESSION.start_document_text_detection(
            Document={"Bytes": image_file.read()}
        )
        job_id = response.get("JobId")

        # Wait for job completion (simplified, real code should handle timeouts)
        while True:
            result = SESSION.get_document_text_detection(JobId=job_id)
            status = result.get("JobStatus")
            if status == "SUCCEEDED":
                break
            elif status == "FAILED":
                raise RuntimeError("Document processing failed")

    blocks = result.get("Blocks")
    merchant = None
    tax = None
    total = None
    items = []

    for block in blocks:
        block_type = block.get("BlockType")
        if block_type == "LINE":
            text = block.get("Text", "").strip().lower()
            if "merchant" in text:
                merchant = text.replace("merchant:", "").strip()
            if "total" in text:
                total = text.replace("total:", "").strip()
            if "tax" in text:
                tax = text.replace("tax:", "").strip()
            # Capture items as lines not containing known keys
            if all(k not in text for k in ["merchant", "total", "tax"]):
                items.append(text)

    return ReceiptFieldsResponse(
        merchant=merchant,
        tax=tax,
        total=total,
        items=items,
    )


if __name__ == "__main__":
    import sys
    from pprint import pprint

    if len(sys.argv) < 2:
        print("Usage: python extract_receipt_fields.py <path_to_receipt>\n")
        sys.exit(1)

    receipt_file = sys.argv[1]
    result = extract_receipt_fields(receipt_file)
    pprint(result.dict())
