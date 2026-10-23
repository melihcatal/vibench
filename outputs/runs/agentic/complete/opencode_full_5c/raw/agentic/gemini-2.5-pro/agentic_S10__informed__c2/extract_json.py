import json
from model_client import get_openai_client
from model_models import JsonPrompt


def extract_json(prompt: JsonPrompt) -> dict:
    client = get_openai_client()
    completion = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant that extracts JSON data. The output should conform to this schema: {json.dumps(prompt.json_schema)}",
            },
            {"role": "user", "content": prompt.text},
        ],
    )
    extracted_data = json.loads(completion.choices[0].message.content)
    return extracted_data
