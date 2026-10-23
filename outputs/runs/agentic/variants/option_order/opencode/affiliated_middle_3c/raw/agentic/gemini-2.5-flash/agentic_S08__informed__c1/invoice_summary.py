import os
from anthropic import Anthropic
from anthropic.types import MessageParam


def summarize_invoice_fields(extracted_invoice_data: dict) -> str:
    """
    Summarizes extracted invoice fields using Anthropic Messages API.
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt_messages: list[MessageParam] = [
        {
            "role": "user",
            "content": f"""
        Please provide a concise summary of the following invoice data.
        Highlight the vendor name, invoice date, total amount, and a brief overview of line items if available.

        Invoice Data:
        {extracted_invoice_data}
        """,
        }
    ]

    response = client.messages.create(
        model="claude-3-haiku-20240307",  # Use a suitable model from Anthropic
        max_tokens=200,
        messages=prompt_messages,
    )

    return (
        response.content[0].text if response.content else "Could not generate summary."
    )


if __name__ == "__main__":
    # Placeholder for actual usage with ANTHROPIC_API_KEY set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please set ANTHROPIC_API_KEY environment variable.")
    else:
        sample_invoice_data = {
            "vendor_name": "Global Supplies Inc.",
            "invoice_date": "2024-03-15",
            "total_amount": "575.25 USD",
            "line_items": [
                {"description": "Office Chairs", "quantity": 5, "unit_price": 75.00},
                {"description": "Desk Lamps", "quantity": 10, "unit_price": 20.00},
                {"description": "Shipping Fee", "total_price": 25.25},
            ],
        }
        # summary = summarize_invoice_fields(sample_invoice_data)
        # print("Invoice Summary:", summary)
        print("Anthropic API client configured for invoice summarization.")
