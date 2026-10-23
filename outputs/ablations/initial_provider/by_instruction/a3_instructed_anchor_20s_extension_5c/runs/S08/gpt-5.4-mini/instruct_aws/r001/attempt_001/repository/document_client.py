import json
import os
from typing import Any, Dict

import boto3

from document_models import DocumentExtractionRequest, DocumentExtractionResponse


class DocumentClient:
    def __init__(self, region_name: str | None = None):
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.textract = boto3.client("textract", region_name=self.region_name)

    def analyze_document(self, request: DocumentExtractionRequest) -> DocumentExtractionResponse:
        if request.document_uri.startswith("s3://"):
            bucket, key = request.document_uri[5:].split("/", 1)
            response = self.textract.analyze_expense(Document={"S3Object": {"Bucket": bucket, "Name": key}})
        else:
            with open(request.document_uri, "rb") as f:
                response = self.textract.analyze_expense(Document={"Bytes": f.read()})
        fields, confidences = self._parse_textract_expense(response)
        return DocumentExtractionResponse(
            provider="aws-textract",
            document_type=request.document_type,
            fields=fields,
            confidences=confidences,
            raw_response=response,
        )

    def _parse_textract_expense(self, response: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, float]]:
        fields: Dict[str, Any] = {}
        confidences: Dict[str, float] = {}
        for doc in response.get("ExpenseDocuments", []):
            for summary in doc.get("SummaryFields", []):
                key = summary.get("Type", {}).get("Text", "").lower()
                value = summary.get("ValueDetection", {}).get("Text")
                confidence = float(summary.get("ValueDetection", {}).get("Confidence", 0.0))
                if key:
                    fields[key] = value
                    confidences[key] = confidence
            line_items = []
            for group in doc.get("LineItemGroups", []):
                for line in group.get("LineItems", []):
                    item = {}
                    for fld in line.get("LineItemExpenseFields", []):
                        field_name = fld.get("Type", {}).get("Text", "").lower()
                        item[field_name] = fld.get("ValueDetection", {}).get("Text")
                    if item:
                        line_items.append(item)
            if line_items:
                fields["line_items"] = line_items
        return fields, confidences


def load_config() -> Dict[str, Any]:
    return {
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "output_bucket": os.getenv("AWS_OUTPUT_BUCKET"),
    }
