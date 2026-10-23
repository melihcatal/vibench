import os
from typing import Dict, Any
import google.generativeai as genai
from document_models import InvoiceData


def summarize_invoice_fields(invoice_data: InvoiceData) -> str:
    """
    Summarize extracted invoice fields using Google Gemini API.

    Args:
        invoice_data: InvoiceData object with extracted fields

    Returns:
        Summary text
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Summarize this invoice information:
    
    Vendor: {invoice_data.vendor_name}
    Invoice Date: {invoice_data.invoice_date}
    Invoice Number: {invoice_data.invoice_number}
    Total Amount: ${invoice_data.total_amount:.2f}
    Tax Amount: ${invoice_data.tax_amount:.2f}
    Subtotal: ${invoice_data.subtotal:.2f}
    Number of Line Items: {len(invoice_data.line_items)}
    
    Provide a concise 2-3 sentence summary highlighting key details.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Failed to generate summary using Google Gemini API: {e}")


def analyze_invoice_patterns(invoice_data: InvoiceData) -> Dict[str, Any]:
    """
    Analyze invoice patterns and provide insights using Google Gemini API.

    Args:
        invoice_data: InvoiceData object

    Returns:
        Dictionary with analysis results
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    line_items_text = ""
    for i, item in enumerate(invoice_data.line_items[:5], 1):
        line_items_text += f"{i}. {item.description}: {item.quantity} x ${item.unit_price:.2f} = ${item.total_price:.2f}\n"

    prompt = f"""
    Analyze this invoice and provide insights:
    
    Vendor: {invoice_data.vendor_name}
    Invoice Date: {invoice_data.invoice_date}
    Total Amount: ${invoice_data.total_amount:.2f}
    Tax Rate: {invoice_data.tax_amount / invoice_data.subtotal * 100 if invoice_data.subtotal > 0 else 0:.1f}%
    
    Top Line Items:
    {line_items_text}
    
    Provide analysis in JSON format with these keys:
    - vendor_category: Categorize the vendor (e.g., software, consulting, office_supplies)
    - payment_urgency: Estimate payment urgency (high, medium, low)
    - expense_type: Categorize expense type (operational, capital, travel, etc.)
    - anomalies: List any anomalies or unusual patterns
    - recommendations: List 1-2 recommendations
    """

    try:
        response = model.generate_content(prompt)

        analysis_text = response.text

        import json

        try:
            analysis_json = json.loads(analysis_text)
        except json.JSONDecodeError:
            analysis_json = {
                "summary": analysis_text,
                "vendor_category": "unknown",
                "payment_urgency": "medium",
                "expense_type": "operational",
                "anomalies": [],
                "recommendations": [],
            }

        return analysis_json

    except Exception as e:
        raise Exception(f"Failed to analyze invoice using Google Gemini API: {e}")


def generate_invoice_report(invoice_data: InvoiceData) -> str:
    """
    Generate a comprehensive invoice report using Google Gemini API.

    Args:
        invoice_data: InvoiceData object

    Returns:
        Markdown formatted report
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    line_items_table = (
        "| Description | Quantity | Unit Price | Total |\n|---|---|---|---|\n"
    )
    for item in invoice_data.line_items:
        line_items_table += f"| {item.description} | {item.quantity} | ${item.unit_price:.2f} | ${item.total_price:.2f} |\n"

    prompt = f"""
    Generate a professional invoice report in markdown format:
    
    # Invoice Report
    
    ## Basic Information
    - **Vendor**: {invoice_data.vendor_name}
    - **Invoice Date**: {invoice_data.invoice_date}
    - **Invoice Number**: {invoice_data.invoice_number}
    
    ## Financial Summary
    - **Subtotal**: ${invoice_data.subtotal:.2f}
    - **Tax**: ${invoice_data.tax_amount:.2f}
    - **Total**: ${invoice_data.total_amount:.2f}
    
    ## Line Items
    {line_items_table}
    
    ## Confidence Metrics
    - **Extraction Confidence**: {invoice_data.confidence_score:.1%}
    - **Field Completeness**: {"High" if len(invoice_data.extracted_fields) >= 5 else "Medium" if len(invoice_data.extracted_fields) >= 3 else "Low"}
    
    Add sections for:
    1. Vendor Analysis
    2. Payment Timeline
    3. Compliance Check
    4. Recommendations
    
    Format as proper markdown with headings and bullet points.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(
            f"Failed to generate invoice report using Google Gemini API: {e}"
        )
