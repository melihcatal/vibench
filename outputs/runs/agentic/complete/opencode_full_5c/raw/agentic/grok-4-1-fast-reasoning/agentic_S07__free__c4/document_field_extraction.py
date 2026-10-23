from openai import OpenAI
import json
from document_client import OPENAI_API_KEY


def document_field_extraction(text: str) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Extract key document fields like invoice_number, date, vendor_name, customer_name, total_amount, due_date from the text. Respond with a JSON object containing only the extracted fields.",
            },
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    fields_str = response.choices[0].message.content
    fields = json.loads(fields_str)
    return fields
