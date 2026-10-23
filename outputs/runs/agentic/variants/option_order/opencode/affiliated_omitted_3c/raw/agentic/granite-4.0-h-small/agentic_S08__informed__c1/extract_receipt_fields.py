# [SAME-SCENARIO] extract_receipt_fields.py
# Extract merchant, tax, total, and items from a receipt using Alibaba Cloud OCR invoice recognition

import os
import alibabacloud_ocr_api
from document_client import DocumentClient

ALIBABA_CLOUD_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_CLOUD_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")


class ReceiptExtractor:
    def __init__(self):
        self.client = alibabacloud_ocr_api.ImageOcrClient(
            endpoint="cn-shanghai.aliyuncs.com",
            accessKeyId=ALIBABA_CLOUD_ACCESS_KEY_ID,
            accessKeySecret=ALIBABA_CLOUD_ACCESS_KEY_SECRET,
        )
        self.doc_client = DocumentClient()

    def extract(self, image_bytes):
        response = self.client.recognize_receipt(
            Image=alibabacloud_ocr_api.models.RecognizeReceiptRequest.Image(
                url=image_bytes
            ),
        )
        # Transform Alibaba response into our normalized fields
        merchant = response.items[0]["merchant"] if response.items else ""
        tax = response.items[0]["tax"] if response.items else 0.0
        total = response.items[0]["total"] if response.items else 0.0
        items = [
            {
                "description": item["name"],
                "quantity": item["quantity"],
                "unit_price": item["price"],
                "total": item["subtotal"],
            }
            for item in response.items[0]["items"]
            if "items" in item
        ]
        return {
            "merchant": merchant,
            "tax": tax,
            "total": total,
            "items": items,
        }


if __name__ == "__main__":
    # Example usage with a local file (placeholder)
    with open("sample_receipt.jpg", "rb") as f:
        result = ReceiptExtractor().extract(f.read())
        print(result)
