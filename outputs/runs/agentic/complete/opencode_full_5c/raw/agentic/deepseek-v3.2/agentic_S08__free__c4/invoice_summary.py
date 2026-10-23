import os
from typing import Dict, Any
import json
from anthropic import Anthropic


def summarize_invoice_fields(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summarize extracted invoice fields using Anthropic Claude.
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    invoice_json = json.dumps(invoice_data, indent=2)

    prompt = f"""
    Analyze this extracted invoice data and provide a concise summary:
    
    {invoice_json}
    
    Provide a summary with:
    1. Key vendor information
    2. Total amount and currency
    3. Number of line items
    4. Date of invoice
    5. Any notable patterns or anomalies
    6. Overall assessment of data completeness
    
    Return the summary as a JSON object with these fields:
    - vendor_summary: string
    - amount_summary: string  
    - line_items_summary: string
    - date_info: string
    - anomalies: array of strings
    - completeness_score: number between 0 and 1
    - overall_assessment: string
    """

    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )

    summary_text = response.content[0].text

    try:
        summary_json = json.loads(summary_text)
    except json.JSONDecodeError:
        summary_json = {
            "vendor_summary": "Vendor information extracted",
            "amount_summary": f"Total: {invoice_data.get('total', 'N/A')} {invoice_data.get('currency', 'USD')}",
            "line_items_summary": f"{len(invoice_data.get('line_items', []))} line items",
            "date_info": f"Date: {invoice_data.get('date', 'N/A')}",
            "anomalies": [],
            "completeness_score": 0.7,
            "overall_assessment": "Invoice data extracted with moderate completeness",
        }

    summary_json["provider"] = "anthropic_claude"
    summary_json["model"] = "claude-3-sonnet-20240229"

    if "total" in invoice_data:
        summary_json["total_amount"] = invoice_data["total"]
    if "currency" in invoice_data:
        summary_json["currency"] = invoice_data["currency"]
    if "line_items" in invoice_data:
        summary_json["line_item_count"] = len(invoice_data["line_items"])

    line_items_total = 0
    for item in invoice_data.get("line_items", []):
        if "amount" in item and item["amount"]:
            line_items_total += item["amount"]
        elif (
            "quantity" in item
            and item["quantity"]
            and "unit_price" in item
            and item["unit_price"]
        ):
            line_items_total += item["quantity"] * item["unit_price"]

    summary_json["calculated_total"] = line_items_total

    if "total" in invoice_data and invoice_data["total"]:
        total_diff = abs(invoice_data["total"] - line_items_total)
        summary_json["total_consistency"] = total_diff < 0.01

    return summary_json
