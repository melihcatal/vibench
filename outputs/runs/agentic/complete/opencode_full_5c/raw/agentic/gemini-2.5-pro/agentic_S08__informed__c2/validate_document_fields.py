from typing import Union, Dict, Any
import boto3
from document_models import Invoice, Receipt


def validate_document_fields(
    document: Union[Invoice, Receipt], file_path: str, confidence_threshold: float = 0.9
) -> Dict[str, Any]:
    """
    Validates fields of an extracted document. If total confidence is low,
    it cross-references with AWS Textract.
    """
    validation_result = {"passed": True, "messages": []}

    doc_dict = document.raw_document or {}
    total_field_info = {}

    if isinstance(document, Invoice):
        total_field_info = doc_dict.get("fields", {}).get("InvoiceTotal", {})
    elif isinstance(document, Receipt):
        total_field_info = doc_dict.get("fields", {}).get("Total", {})

    confidence = total_field_info.get("confidence", 1.0)

    if confidence < confidence_threshold:
        validation_result["messages"].append(
            f"Low confidence ({confidence:.2f}) for total. Cross-validating with AWS Textract."
        )

        try:
            textract_client = boto3.client("textract")
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            response = textract_client.analyze_expense(Document={"Bytes": file_bytes})

            textract_total = None
            for expense_doc in response.get("ExpenseDocuments", []):
                for summary_field in expense_doc.get("SummaryFields", []):
                    if summary_field.get("Type", {}).get("Text") == "TOTAL":
                        textract_total = float(
                            summary_field.get("ValueDetection", {}).get("Text")
                        )
                        break
                if textract_total is not None:
                    break

            original_total = (
                document.total_amount
                if isinstance(document, Invoice)
                else document.total
            )

            if (
                textract_total is not None
                and abs(original_total - textract_total) > 0.01
            ):
                validation_result["passed"] = False
                validation_result["messages"].append(
                    f"Discrepancy found. Original total: {original_total}, Textract total: {textract_total}"
                )
            else:
                validation_result["messages"].append(
                    "AWS Textract validation confirmed the total."
                )

        except Exception as e:
            validation_result["passed"] = False
            validation_result["messages"].append(
                f"Error during AWS Textract validation: {e}"
            )

    return validation_result
