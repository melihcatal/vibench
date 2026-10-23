import openai
import os
import json
from document_models import FieldsResult


def document_field_extraction(text: str) -> FieldsResult:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": "Extract key fields from this document text as JSON. Possible fields: name, date, address, amount, email, phone. If not found, use null. Output only valid JSON.\\n\\nText: "
                + text,
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    content = completion.choices[0].message.content
    fields = json.loads(content)
    return {"fields": fields}
