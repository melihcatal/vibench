import json


def coerce_mapping(value):
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {"value": parsed}
        except Exception:
            return {"value": value}
    return {"value": value}


def normalize_items(items):
    output = []
    for item in items or []:
        data = coerce_mapping(item)
        output.append(
            {
                "description": data.get("description")
                or data.get("name")
                or data.get("item")
                or "",
                "quantity": data.get("quantity"),
                "unit_price": data.get("unit_price") or data.get("price"),
                "amount": data.get("amount") or data.get("total"),
            }
        )
    return output


def normalize_document_result(payload):
    data = coerce_mapping(payload)
    return {
        "vendor": data.get("vendor") or data.get("merchant") or data.get("supplier"),
        "date": data.get("date")
        or data.get("invoice_date")
        or data.get("transaction_date"),
        "total": data.get("total")
        or data.get("amount_total")
        or data.get("grand_total"),
        "tax": data.get("tax") or data.get("tax_total") or data.get("vat"),
        "currency": data.get("currency"),
        "notes": data.get("notes") or data.get("memo") or data.get("description"),
        "items": normalize_items(data.get("items") or data.get("line_items") or []),
        "confidence": data.get("confidence"),
    }
