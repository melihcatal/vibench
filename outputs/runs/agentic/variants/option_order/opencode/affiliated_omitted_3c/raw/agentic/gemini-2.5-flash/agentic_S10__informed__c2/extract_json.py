import os
from openai import OpenAI


def extract_json(text: str) -> dict:
    """
    Calls a hosted LLM (OpenAI) to extract structured JSON from text.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Provider-specific model ID
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that extracts information into JSON format. Respond only with JSON.",
            },
            {
                "role": "user",
                "content": f"Extract the name and age from the following text: {text}. Output as a JSON object with 'name' and 'age' fields.",
            },
        ],
    )
    return response.choices[0].message.content
