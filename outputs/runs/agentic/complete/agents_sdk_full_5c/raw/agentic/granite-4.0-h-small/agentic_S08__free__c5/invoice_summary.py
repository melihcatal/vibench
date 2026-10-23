from typing import Dict

def invoice_summary(extracted: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a concise summary from a full invoice extraction."""
    summary = {
        "vendor": extracted.get("vendor", "Unknown"),
        "date": extracted.get("date", "N/A"),
        "total_amount": extracted.get("total", 0.0),
        "currency": extracted.get("currency", "USD"),
        "line_item_count": len(extracted.get("line_items", []))
    }
    return summary