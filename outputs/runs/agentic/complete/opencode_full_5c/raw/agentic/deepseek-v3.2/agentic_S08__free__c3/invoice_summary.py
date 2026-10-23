import os
from openai import OpenAI
from document_client import load_config


def summarize_invoice_fields(invoice_data):
    config = load_config()

    client = OpenAI(api_key=config["openai_api_key"])

    vendor = invoice_data.get("vendor", "Unknown Vendor")
    date = invoice_data.get("date", "Unknown Date")
    total = invoice_data.get("total", "0")
    line_items = invoice_data.get("line_items", [])

    line_items_text = ""
    for i, item in enumerate(line_items, 1):
        desc = item.get("description", "No description")
        qty = item.get("quantity", "0")
        price = item.get("unit_price", "0")
        amount = item.get("amount", "0")
        line_items_text += f"{i}. {desc}: {qty} x ${price} = ${amount}\n"

    prompt = f"""Summarize this invoice extraction:

Vendor: {vendor}
Date: {date}
Total Amount: ${total}

Line Items:
{line_items_text}

Please provide a concise summary including:
1. Main vendor and date
2. Total amount
3. Number of line items
4. Any notable items or patterns
5. Overall assessment of the invoice

Keep the summary to 3-4 sentences maximum."""

    response = client.chat.completions.create(
        model=config["openai_model"],
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes extracted invoice data.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=200,
    )

    summary = response.choices[0].message.content

    return {
        "vendor": vendor,
        "date": date,
        "total_amount": total,
        "line_item_count": len(line_items),
        "summary": summary,
        "model_used": config["openai_model"],
    }
