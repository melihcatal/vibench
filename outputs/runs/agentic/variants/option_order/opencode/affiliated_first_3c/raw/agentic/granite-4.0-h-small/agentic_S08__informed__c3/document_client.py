import os
import boto3
from mindee import MindeeClient
import requests


class DocumentClient:
    """Local helper utilities for Structured Document Extraction.","""

    def __init__(self):
        # Load AWS credentials from environment variables
        self.textract = boto3.client("textract")
        # Mindee requires API key, also loaded from env or set here.
        self.mindee_key = os.getenv("MINDEE_API_KEY")
        self.mindee = MindeeClient(api_key=self.mindee_key)
        # Generic HTTP client for services like Azure
        self.http = requests.Session()
        # Set default headers for Azure (example)
        self.http.headers.update({"Content-Type": "application/octet-stream"})

    def analyze_expense_textract(self, pdf_bytes):
        """Wrapper around Textract AnalyzeExpense returning a simple dict.","""
        response = self.textract.analyze_expense(Document={"Bytes": pdf_bytes})
        expense = response["ExpenseIndices"][0]
        fields = {}
        for block in response["Blocks"]:
            if block["BlockType"] == "KEY_VALUE_SET" and block["EntityTypes"]:
                key = None
                value = None
                for rel in block.get("Relationships", []):
                    if rel["Type"] == "CHILD":
                        for child_id in rel["Ids"]:
                            child = next(
                                (b for b in response["Blocks"] if b["Id"] == child_id),
                                None,
                            )
                            if child and child["BlockType"] == "KEY" and not key:
                                key = child["Text"].strip()
                            elif child and child["BlockType"] == "VALUE" and not value:
                                value = child["Text"].strip()
                if key and value:
                    fields[key] = {
                        "value": value,
                        "confidence": 0.85,
                    }  # placeholder confidence
        return {
            "vendor": fields.get("Vendor", "")["value"],
            "date": fields.get("Date", "")["value"],
            "total": float(fields.get("Total", "")["value"]),
            "line_items": [],
        }

    def analyze_receipt_mindee(self, image_bytes):
        """Wrapper around Mindee Invoice OCR returning a simple dict.","""
        client = MindeeClient(api_key=self.mindee_key)
        invoice = client.invoice.parse(file=image_bytes)
        output = invoice.original_doc.data
        return {
            "merchant": output["merchant"]["name"],
            "tax": output.get("tax", {}).get("total") or "",
            "total": output.get("total", {}).get("amount") or "",
            "items": [
                {
                    "description": l.get("description"),
                    "quantity": l.get("quantity"),
                    "amount": l.get("amount"),
                }
                for l in output.get("items", [])
            ],
        }

    def call_azure_invoice(self, pdf_bytes):
        """Example call to Azure Document Intelligence prebuilt invoice endpoint.","""
        endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
        headers = {"Ocp-Apim-Subscription-Key": key}
        data = {
            "url": "s3://temp/pdf.pdf"
        }  # placeholder, real implementation would upload
        resp = self.http.post(
            f"{endpoint}/prebuilts/invoice", headers=headers, json=data
        )
        return resp.json()
