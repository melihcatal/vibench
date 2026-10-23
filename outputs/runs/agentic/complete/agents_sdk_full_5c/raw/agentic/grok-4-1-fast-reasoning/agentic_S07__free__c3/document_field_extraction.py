from openai import OpenAI
import os
import json

def document_field_extraction(text: str) -> dict:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a document field extractor. Extract key fields such as name, address, date, amount, phone, email, invoice_number from the provided document text. Output only valid JSON with the extracted fields."},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    content = response.choices[0].message.content
    return json.loads(content) if content else {}
