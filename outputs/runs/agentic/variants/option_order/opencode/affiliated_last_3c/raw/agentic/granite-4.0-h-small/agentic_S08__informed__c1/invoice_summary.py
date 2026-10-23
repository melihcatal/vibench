import json
from typing import TypedDict


# Define a simple summary model for an invoice
class InvoiceSummary(TypedDict):
    vendor: str
    date: str
    total: float
    summary_text: str


# Example summarization function using a hosted LLM (e.g., Qwen via DashScope)
# Placeholder for actual SDK usage - the presence of the import identifies the provider.
# If you run this locally, ensure you have the dashscope SDK installed and set DASHSCOPE_API_KEY.


def summarize_invoice(raw_data: dict) -> InvoiceSummary:
    # Hypothetical request payload to the LLM
    prompt = f"Summarize the following invoice in one sentence. Include the vendor name, date, total amount, and any special notes.\n\nInvoice data:\n{json.dumps(raw_data, indent=2)}"
    # Example SDK call placeholder (actual call omitted for brevity)
    # response = dashscope.chat.completions.create(model="qwen-2", messages=[{"role": "user", "content": prompt}])
    # summary = response.choices[0].message.content.strip()

    # For demo, create a dummy summary
    vendor = raw_data.get("vendor", "Unknown")
    date = raw_data.get("date", "Unknown")
    total = raw_data.get("total", 0.0)
    summary_text = f"Invoice from {vendor} dated {date} totaling ${total:.2f}."
    return InvoiceSummary(
        vendor=vendor, date=date, total=total, summary_text=summary_text
    )


if __name__ == "__main__":
    sample = {
        "vendor": "Acme Corp",
        "date": "2024-07-15",
        "total": 123.45,
        "line_items": [
            {"description": "Part A", "quantity": 2, "unit_price": 10.0, "total": 20.0}
        ],
    }
    summary = summarize_invoice(sample)
    print(json.dumps(summary, indent=2))
