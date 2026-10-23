import json
from model_client import get_openai_client


def extract_json(text: str) -> dict:
    """
    Calls a hosted LLM to extract structured JSON from text.
    """
    client = get_openai_client()

    prompt = f"""
    Extract the user's name and contact information (email and phone)
    from the following text and return it as a valid JSON object.
    The JSON object should have keys "name", "email", and "phone".

    Text:
    "{text}"
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    if response.choices:
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {}
    return {}
