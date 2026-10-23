def invoice_summary(normalized):
    """Create a concise human‑readable summary of an invoice."""
    vendor = normalized['vendor_or_merchant']
    date = normalized['date']
    total = normalized['total']
    line_items = normalized['line_items_or_items']
    
    items_str = \"\\n    \".join(f\"{it.get('description','<no desc>')}: ${it.get('price','0')}\" for it in line_items)
    return (f\"Invoice Summary\\nVendor: {vendor}\\nDate: {date}\\nTotal: ${total:.2f}\\nItems:\\n    {items_str}\")