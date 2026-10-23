import boto3
from typing import Dict, Any, Optional
import os

class ReceiptExtractor:
    def __init__(self):
        self.client = boto3.client(
            "textract",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )

    def extract_fields(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, "rb") as file:
            document_content = file.read()

        response = self.client.analyze_expense(Document={'Bytes': document_content})
        return self._parse_receipt_fields(response)

    def _parse_receipt_fields(self, response: Dict[str, Any]) -> Dict[str, Any]:
        fields = {
            "merchant": self._get_expense_field(response, "VENDOR"),
            "tax": self._get_expense_field(response, "TAX"),
            "total": self._get_expense_field(response, "TOTAL"),
            "items": self._get_items(response),
            "confidence": self._get_confidence(response)
        }
        return fields

    def _get_expense_field(self, response: Dict[str, Any], field_type: str) -> Optional[str]:
        for expense_doc in response.get("ExpenseDocuments", []):
            for summary_field in expense_doc.get("SummaryFields", []):
                if summary_field.get("Type", {}).get("Text") == field_type:
                    return summary_field.get("ValueDetection", {}).get("Text")
        return None

    def _get_items(self, response: Dict[str, Any]) -> list:
        items = []
        for expense_doc in response.get("ExpenseDocuments", []):
            for line_item_group in expense_doc.get("LineItemGroups", []):
                for line_item in line_item_group.get("LineItems", []):
                    item = {
                        "description": self._get_line_item_field(line_item, "DESCRIPTION"),
                        "quantity": self._get_line_item_field(line_item, "QUANTITY"),
                        "price": self._get_line_item_field(line_item, "PRICE"),
                        "amount": self._get_line_item_field(line_item, "AMOUNT")
                    }
                    items.append(item)
        return items

    def _get_line_item_field(self, line_item: Dict[str, Any], field_type: str) -> Optional[str]:
        for line_item_field in line_item.get("LineItemExpenseFields", []):
            if line_item_field.get("Type", {}).get("Text") == field_type:
                return line_item_field.get("ValueDetection", {}).get("Text")
        return None

    def _get_confidence(self, response: Dict[str, Any]) -> float:
        confidence_scores = []
        for expense_doc in response.get("ExpenseDocuments", []):
            for summary_field in expense_doc.get("SummaryFields", []):
                confidence_scores.append(summary_field.get("ValueDetection", {}).get("Confidence", 0))
            for line_item_group in expense_doc.get("LineItemGroups", []):
                for line_item in line_item_group.get("LineItems", []):
                    for line_item_field in line_item.get("LineItemExpenseFields", []):
                        confidence_scores.append(line_item_field.get("ValueDetection", {}).get("Confidence", 0))
        return sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0