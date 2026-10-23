from typing import Dict, List

import openai


def extract_fields(text: str, fields: List[str]) -> Dict[str, str]:
    client = openai.OpenAI()
    prompt = {
        "text": text,
        "fields": fields,
    }
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[{"role": "user", "content": str(prompt)}],
    )
    return {field: response.output_text for field in fields}
