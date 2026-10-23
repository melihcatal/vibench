from typing import List, Dict, Any
from document_models import ExpenseDocument


def validate_expense_document(
    expense_document: ExpenseDocument,
    required_fields: List[str],
    min_confidence: float = 0.7,
) -> ExpenseDocument:
    missing_fields = []
    low_confidence_fields = []

    for field in required_fields:
        if not getattr(expense_document, field):
            missing_fields.append(field)

    if expense_document.raw_extraction_data.get("ExpenseDocuments"):
        for expense_doc_data in expense_document.raw_extraction_data[
            "ExpenseDocuments"
        ]:
            for field_type in ["SummaryFields", "LineItemGroups"]:
                for field_data in (
                    expense_doc_data.get(field_type, [])
                    if isinstance(expense_doc_data.get(field_type), list)
                    else []
                ):
                    if field_type == "SummaryFields":
                        confidence_score = field_data.get("Confidence")
                        field_name = field_data.get("Type", {}).get("Text")
                        if (
                            confidence_score is not None
                            and confidence_score < min_confidence
                        ):
                            low_confidence_fields.append(
                                f"{field_name} (Confidence: {confidence_score})"
                            )
                    elif field_type == "LineItemGroups":
                        for item_block in field_data.get("LineItems", []):
                            for item_field in (
                                item_block.get("LineItemExpenseFields", [])
                                if isinstance(
                                    item_block.get("LineItemExpenseFields"), list
                                )
                                else []
                            ):
                                confidence_score = item_field.get("Confidence")
                                field_name = item_field.get("Type", {}).get("Text")
                                if (
                                    confidence_score is not None
                                    and confidence_score < min_confidence
                                ):
                                    low_confidence_fields.append(
                                        f"Line Item {field_name} (Confidence: {confidence_score})"
                                    )

    if missing_fields:
        expense_document.validation_status = (
            f"Failed: Missing fields: {', '.join(missing_fields)}"
        )
    elif low_confidence_fields:
        expense_document.validation_status = (
            f"Warning: Low confidence fields: {', '.join(low_confidence_fields)}"
        )
    else:
        expense_document.validation_status = "Passed"

    return expense_document
