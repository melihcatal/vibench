import os
from typing import Any, Dict, Iterable, List

import boto3

from document_models import (
    StructuredDocumentRequest,
    StructuredDocumentResponse,
    StructuredField,
    normalize_field_map,
)


class TextractDocumentClient:
    def __init__(self, region_name: str = None):
        self.client = boto3.client(
            "textract", region_name=region_name or os.getenv("AWS_REGION", "us-east-1")
        )

    def analyze_expense(
        self, request: StructuredDocumentRequest
    ) -> StructuredDocumentResponse:
        source: Dict[str, Any]
        if request.document_bytes:
            source = {"Bytes": request.document_bytes}
        else:
            with open(request.file_path, "rb") as f:
                source = {"Bytes": f.read()}
        result = self.client.analyze_expense(Document=source)
        expense_docs = result.get("ExpenseDocuments", [])
        fields: List[StructuredField] = []
        for doc in expense_docs:
            for summary in doc.get("SummaryFields", []):
                fields.append(
                    StructuredField(
                        name=summary.get("Type", {}).get("Text", "field"),
                        value=summary.get("ValueDetection", {}).get("Text"),
                        confidence=float(
                            summary.get("ValueDetection", {}).get("Confidence", 0.0)
                        ),
                    )
                )
            for item in doc.get("LineItemGroups", []):
                for line in item.get("LineItems", []):
                    line_payload = normalize_field_map(
                        {
                            element.get("Type", {}).get("Text", "field"): element.get(
                                "ValueDetection", {}
                            ).get("Text")
                            for element in line.get("LineItemExpenseFields", [])
                        }
                    )
                    fields.append(
                        StructuredField(
                            name="line_item",
                            value=line_payload,
                            confidence=max(
                                [
                                    float(
                                        element.get("ValueDetection", {}).get(
                                            "Confidence", 0.0
                                        )
                                    )
                                    for element in line.get("LineItemExpenseFields", [])
                                ]
                                or [0.0]
                            ),
                        )
                    )
        return StructuredDocumentResponse(
            provider="amazon-textract-analyzeexpense", fields=fields, raw=result
        )
