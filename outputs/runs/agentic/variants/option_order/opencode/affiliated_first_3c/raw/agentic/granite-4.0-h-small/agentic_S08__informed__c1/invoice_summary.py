def summarize_invoice(expense):
    """Generate a concise textual summary of an extracted expense."""
    summary_lines = []
    summary_lines.append(f"Vendor: {expense['vendor']}")
    summary_lines.append(f"Date: {expense['date']}")
    summary_lines.append(f"Total: {expense['total']:.2f}")
    summary_lines.append("Line items:")
    for item in expense["line_items"]:
        summary_lines.append(
            f"  - {item['description']}: qty {item['quantity']} x ${item['unit_price']:.2f} = ${item['amount']:.2f}"
        )
    return "\\n".join(summary_lines)
