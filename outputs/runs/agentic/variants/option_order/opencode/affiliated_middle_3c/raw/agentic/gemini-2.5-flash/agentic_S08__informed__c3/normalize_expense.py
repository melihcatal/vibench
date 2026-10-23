from typing import Dict, Any, Optional
from datetime import date
from google.cloud import documentai_v1 as documentai  # Provider identifiable import
from document_models import NormalizedExpense, LineItem


def normalize_document_ai_output(
    documentai_json: Dict[str, Any], document_type: str = "unknown"
) -> Optional[NormalizedExpense]:
    """
    Normalizes Document AI output into a standard NormalizedExpense schema.
    This function is a scored component, designed to work with Google Document AI output.
    """
    vendor_name = ""
    transaction_date = None
    total_amount = 0.0
    currency = ""
    tax_amount = None
    line_items = []
    notes = ""

    confidence_vendor = 0.0
    confidence_date = 0.0
    confidence_total = 0.0

    if "entities" in documentai_json:
        for entity in documentai_json["entities"]:
            entity_type = entity.get("type")
            mention_text = entity.get("mentionText") or (
                entity.get("textAnchor") and entity["textAnchor"].get("content")
            )
            normalized_value = entity.get("normalizedValue", {})
            confidence = entity.get("confidence", 0.0)

            if entity_type == "vendor_name" or entity_type == "merchant_name":
                vendor_name = mention_text or ""
                confidence_vendor = confidence
            elif (
                entity_type == "purchase_order_date"
                or entity_type == "transaction_date"
            ):
                try:
                    if (
                        "dateValue" in normalized_value
                        and "iso8601Date" in normalized_value["dateValue"]
                    ):
                        transaction_date = date.fromisoformat(
                            normalized_value["dateValue"]["iso8601Date"]
                        )
                except (AttributeError, ValueError):
                    pass
                confidence_date = confidence
            elif entity_type == "total_amount":
                try:
                    if (
                        "moneyValue" in normalized_value
                        and "amount" in normalized_value["moneyValue"]
                    ):
                        total_amount = float(normalized_value["moneyValue"]["amount"])
                        currency = normalized_value["moneyValue"].get("currency", "")
                except (AttributeError, ValueError):
                    pass
                confidence_total = confidence
            elif entity_type == "total_tax_amount":
                try:
                    if (
                        "moneyValue" in normalized_value
                        and "amount" in normalized_value["moneyValue"]
                    ):
                        tax_amount = float(normalized_value["moneyValue"]["amount"])
                except (AttributeError, ValueError):
                    pass
            elif entity_type == "line_item":
                item_description = ""
                item_quantity = 0.0
                item_unit_price = 0.0
                item_total_price = 0.0
                for prop in entity.get("properties", []):
                    prop_type = prop.get("type")
                    prop_mention_text = prop.get("mentionText") or (
                        prop.get("textAnchor") and prop["textAnchor"].get("content")
                    )
                    prop_normalized_value = prop.get("normalizedValue", {})

                    if prop_type == "description":
                        item_description = prop_mention_text or ""
                    elif prop_type == "quantity":
                        try:
                            item_quantity = float(
                                prop_normalized_value.get("floatValue", 0.0)
                            )
                        except (AttributeError, ValueError):
                            pass
                    elif prop_type == "unit_price":
                        try:
                            if "moneyValue" in prop_normalized_value:
                                item_unit_price = float(
                                    prop_normalized_value["moneyValue"].get(
                                        "amount", 0.0
                                    )
                                )
                        except (AttributeError, ValueError):
                            pass
                    elif prop_type == "amount":  # total amount for line item
                        try:
                            if "moneyValue" in prop_normalized_value:
                                item_total_price = float(
                                    prop_normalized_value["moneyValue"].get(
                                        "amount", 0.0
                                    )
                                )
                        except (AttributeError, ValueError):
                            pass
                if item_description or item_total_price:
                    line_items.append(
                        LineItem(
                            description=item_description,
                            quantity=item_quantity,
                            unit_price=item_unit_price,
                            total_price=item_total_price,
                        )
                    )
            elif entity_type == "invoice_number" or entity_type == "receipt_number":
                if mention_text:
                    if not notes:
                        notes = (
                            f"{entity_type.replace('_', ' ').title()}: {mention_text}"
                        )
                    else:
                        notes += (
                            f", {entity_type.replace('_', ' ').title()}: {mention_text}"
                        )

    if not transaction_date:
        transaction_date = date.today()  # Default to today if not found

    try:
        return NormalizedExpense(
            vendor_name=vendor_name,
            transaction_date=transaction_date,
            total_amount=total_amount,
            currency=currency,
            tax_amount=tax_amount,
            line_items=line_items,
            document_type=document_type,
            notes=notes,
            confidence_vendor=confidence_vendor,
            confidence_date=confidence_date,
            confidence_total=confidence_total,
        )
    except Exception as e:
        print(f"Error creating NormalizedExpense model: {e}")
        return None
