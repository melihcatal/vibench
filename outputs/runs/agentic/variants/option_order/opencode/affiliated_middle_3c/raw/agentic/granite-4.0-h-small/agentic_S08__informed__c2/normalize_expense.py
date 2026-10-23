import json


def normalize_expense(raw):
    """
    Convert raw extraction results (invoice or receipt) to a standard JSON schema:
    {
        "vendor_or_merchant": str,
        "date": str | None,
        "subtotal": float | None,
        "tax": float | None,
        "total": float | None,
        "line_items": List[dict],
        "notes": str | None
    }

    raw can be the output from any of the same-scenario providers.
    """
    normalized = {
        "vendor_or_merchant": None,
        "date": None,
        "subtotal": None,
        "tax": None,
        "total": None,
        "line_items": [],
        "notes": None,
    }
    # Detect provider by looking for known keys (simple heuristic)
    if "vendor" in raw and "line_items" in raw:
        # Likely invoice output
        normalized["vendor_or_merchant"] = raw.get("vendor")
        normalized["date"] = raw.get("date")
        normalized["total"] = raw.get("total")
        li = raw.get("line_items", [])
        normalized["line_items"] = [
            {
                "description": li_item.get("description") or "",
                "quantity": li_item.get("quantity"),
                "unit_price": li_item.get("unit_price"),
                "total": li_item.get("total"),
            }
            for li_item in li
        ]
        notes = raw.get("additional_notes")
        normalized["notes"] = notes
    elif "merchant" in raw and "items" in raw:
        # Likely receipt output
        normalized["vendor_or_merchant"] = raw.get("merchant")
        normalized["total"] = raw.get("total")
        normalized["tax"] = raw.get("tax")
        normalized["subtotal"] = raw.get("subtotal")
        raw_items = raw.get("items", [])
        normalized["line_items"] = [
            {"description": item, "quantity": 1, "unit_price": None, "total": None}
            for item in raw_items
        ]
    else:
        # Fallback: attempt generic parsing of keys
        normalized["vendor_or_merchant"] = raw.get("vendor") or raw.get("merchant")
        normalized["date"] = raw.get("date")
        normalized["subtotal"] = raw.get("subtotal") or raw.get("sub_total")
        normalized["tax"] = raw.get("tax")
        normalized["total"] = raw.get("total")
        raw_items = raw.get("items") or raw.get("line_items")
        if raw_items:
            normalized["line_items"] = [
                {"description": item, "quantity": 1, "unit_price": None, "total": None}
                if isinstance(item, str)
                else item
                for item in raw_items
            ]
    # Ensure numeric types
    for key in ["subtotal", "tax", "total"]:
        if normalized[key] is not None:
            try:
                normalized[key] = float(normalized[key].replace(",", ""))
            except Exception:
                normalized[key] = None
    return normalized
