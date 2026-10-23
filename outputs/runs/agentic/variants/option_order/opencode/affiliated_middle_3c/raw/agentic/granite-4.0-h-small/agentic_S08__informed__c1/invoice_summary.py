import json
from typing import Dict

def invoice_summary(raw_data: Dict[str, any]) -> str:
    """Create a concise human‑readable summary of an invoice.

    Uses the normalised expense schema produced by
    `normalize_expense.py`.
    """
    summary_lines = [f"Invoice from {raw_data['vendor']} on {raw_data['date']}\n",
                     f"Total amount: ${raw_data['total']:.2f}"]
    if raw_data.get('line_items'):
        summary_lines.append("Line items:\")
        for item in raw_data['line_items']:
            summary_lines.append(
                f"- {item['description']}: ${item['total']:.2f}"
            )
    else:
        summary_lines.append("No line‑items detected.")
    return "\n".join(summary_lines)

# Small demo when running the file directly
if __name__ == "__main__":
    sample = {
        "vendor": "Acme Corp",
        "date": "2024‑07‑15",
        "total": 125.50,
        "line_items": [
            {"description": "Widget A", "total": 90.00},
            {"description": "Widget B", "total": 35.50}
        ]
    }
    print(invoice_summary(sample))