import os
import json
from openai import OpenAI

def extract_json(text: str) -> dict:
    """
    Calls a hosted LLM (OpenAI's GPT-3.5 Turbo) to extract structured JSON from text.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts information into a JSON object. Always respond with a JSON object."},
            {"role": "user", "content": f"Extract the name and age from the following text:\n\n{text}\n\nRespond with a JSON object like: {{\"name\": \"<name>\", \"age\": <age>}}"}
        ],
        response_format={ "type": "json_object" },
        max_tokens=200,
        temperature=0.0,
    )
    return json.loads(response.choices[0].message.content.strip())
