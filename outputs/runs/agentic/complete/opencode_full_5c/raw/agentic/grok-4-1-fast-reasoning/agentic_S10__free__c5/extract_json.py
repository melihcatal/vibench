import json
from model_client import openai_client


def extract_json(text: str, instructions: str) -> dict:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at extracting structured data. Respond only with valid JSON matching the instructions.",
            },
            {
                "role": "user",
                "content": f"{instructions}\n\nText to extract from:\n{text}",
            },
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    content = response.choices[0].message.content.strip()
    return json.loads(content)
