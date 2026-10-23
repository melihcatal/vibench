import google.generativeai as genai
from document_models import NormalizedExpense
import os
import json

def get_gemini_model_for_summary():
    """Configures and returns a Gemini Pro model instance."""
    # Ensure GOOGLE_API_KEY environment variable is set.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel('gemini-pro')

def summarize_invoice_fields(expense_data: NormalizedExpense) -> str:
    """
    Summarizes extracted invoice fields using Gemini.
    """
    if expense_data.document_type != "invoice":
        return "Not an invoice document, skipping summary."

    model = get_gemini_model_for_summary()

    # Prepare data for the prompt
    data_for_prompt = expense_data.dict(exclude_unset=True)
    
    # Remove raw_text if too long, as it might hit token limits or be less relevant for summary
    if 'raw_text' in data_for_prompt:
        data_for_prompt['raw_text'] = data_for_prompt['raw_text'][:500] + "..." if len(data_for_prompt['raw_text']) > 500 else data_for_prompt['raw_text']

    prompt_parts = [
        f"Summarize the key information from the following invoice data. Focus on vendor, date, total amount, "
        f"and a brief overview of line items if present. Keep it concise, no more than 3 sentences.
"
        f"```json
{json.dumps(data_for_prompt, indent=2)}
```
"
        f"Summary:"
    ]

    try:
        response = model.generate_content(prompt_parts)
        return response.text.strip()
    except Exception as e:
        return f"Error summarizing invoice: {e}"

if __name__ == '__main__':
    # Example usage:
    # Set GOOGLE_API_KEY environment variable
    #
    # example_invoice = NormalizedExpense(
    #     document_type="invoice",
    #     vendor_name="Tech Solutions Inc.",
    #     transaction_date="2023-11-01",
    #     total_amount=500.25,
    #     currency="USD",
    #     invoice_number="INV-2023-001",
    #     line_items=[
    #         LineItem(description="Software License", quantity=1, unit_price=400.00, total_price=400.00),
    #         LineItem(description="Support Services", quantity=1, unit_price=100.25, total_price=100.25)
    #     ],
    #     raw_text="This is a raw text from the invoice of Tech Solutions Inc. for software and services on 2023-11-01."
    # )
    #
    # summary = summarize_invoice_fields(example_invoice)
    # print(summary)
    pass
