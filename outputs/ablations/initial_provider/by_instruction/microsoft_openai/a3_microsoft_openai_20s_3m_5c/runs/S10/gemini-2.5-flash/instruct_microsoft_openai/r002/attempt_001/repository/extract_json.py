import os
import openai
import json

def extract_json(text: str, schema: dict) -> dict:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

    client = openai.OpenAI(
        api_key=openai.api_key,
        base_url=openai.api_base,
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts information into JSON format. The user will provide a text and a JSON schema. Your task is to extract the information from the text according to the schema."},
            {"role": "user", "content": f"Extract information from the following text into JSON format according to the provided schema. Text: {text}\nSchema: {json.dumps(schema)}"}
        ],
        response_format={ "type": "json_object" }
    )
    return json.loads(response.choices[0].message.content)
