import os
from typing import Dict, Any
from document_models import ExpenseRecord


def summarize_invoice_fields(extracted_invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summarize extracted invoice fields using Anthropic Claude.
    """
    import anthropic

    # Initialize Anthropic client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    # Convert extracted data to string for summarization
    invoice_data_str = str(extracted_invoice_data)

    prompt = f"""You are an expert invoice analyst. Analyze the following extracted invoice data and provide a concise summary.

Extracted Invoice Data:
{invoice_data_str}

Please provide a summary with these sections:
1. **Vendor Information**: Name, address, tax ID if available
2. **Invoice Details**: Date, invoice total, currency
3. **Line Items Summary**: Number of items, total quantity, average price per item
4. **Key Observations**: Any notable patterns, missing information, or data quality issues
5. **Recommendations**: Suggestions for expense categorization or follow-up actions

Format the response as a structured JSON object with these fields:
- vendor_summary (string)
- invoice_summary (string) 
- line_items_summary (string)
- observations (array of strings)
- recommendations (array of strings)
- confidence_score (float between 0 and 1)
"""

    try:
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        # Parse the JSON response
        import json

        try:
            summary_data = json.loads(summary_text)
        except json.JSONDecodeError:
            # If response isn't valid JSON, create a basic summary
            summary_data = {
                "vendor_summary": "Vendor information extracted from invoice",
                "invoice_summary": f"Invoice total: {extracted_invoice_data.get('total', 'N/A')}",
                "line_items_summary": f"{len(extracted_invoice_data.get('line_items', []))} line items",
                "observations": ["Invoice data extracted successfully"],
                "recommendations": ["Review extracted fields for accuracy"],
                "confidence_score": 0.8,
            }

        # Add metadata
        summary_data["summary_provider"] = "anthropic"
        summary_data["summary_model"] = "claude-3-opus-20240229"
        summary_data["summary_timestamp"] = os.getenv("SUMMARY_TIMESTAMP", "")

        # Calculate additional metrics
        if "line_items" in extracted_invoice_data:
            line_items = extracted_invoice_data["line_items"]
            total_quantity = 0
            total_amount = 0
            item_count = len(line_items)

            for item in line_items:
                if "quantity" in item and item["quantity"]:
                    try:
                        total_quantity += float(item["quantity"])
                    except (ValueError, TypeError):
                        pass
                if "amount" in item and item["amount"]:
                    try:
                        total_amount += float(item["amount"])
                    except (ValueError, TypeError):
                        pass

            summary_data["metrics"] = {
                "item_count": item_count,
                "total_quantity": total_quantity,
                "total_line_items_amount": total_amount,
                "average_item_amount": total_amount / item_count
                if item_count > 0
                else 0,
            }

        # Add vendor information if available
        if "vendor" in extracted_invoice_data:
            vendor = extracted_invoice_data["vendor"]
            summary_data["vendor_details"] = {
                "name": vendor.get("name"),
                "address": vendor.get("address"),
                "tax_id": vendor.get("tax_id"),
            }

        # Add invoice totals
        if "total" in extracted_invoice_data:
            summary_data["invoice_totals"] = {
                "invoice_total": extracted_invoice_data.get("total"),
                "currency": extracted_invoice_data.get("currency", "USD"),
            }

        return summary_data

    except Exception as e:
        # Fallback summary if API call fails
        return {
            "vendor_summary": "Error generating summary",
            "invoice_summary": f"Error: {str(e)}",
            "line_items_summary": "Unable to summarize line items",
            "observations": [f"API error: {str(e)}"],
            "recommendations": ["Check API configuration and try again"],
            "confidence_score": 0.0,
            "summary_provider": "anthropic",
            "summary_model": "claude-3-opus-20240229",
            "error": str(e),
        }
