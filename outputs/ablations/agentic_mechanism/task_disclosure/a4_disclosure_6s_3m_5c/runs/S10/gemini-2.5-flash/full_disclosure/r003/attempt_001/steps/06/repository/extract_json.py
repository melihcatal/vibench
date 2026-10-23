import openai
import os
import json

def extract_json_from_text(text: str) -> dict:
    """
    Calls a hosted LLM (OpenAI) to extract structured JSON from text.

    Args:
        text: The input text from which to extract JSON.

    Returns:
        A dictionary representing the extracted JSON.
    """
    client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # OpenAI model identifier
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
            {"role": "user", "content": f"Extract structured JSON from the following text: {text}"}
        ]
    )
    
    # Assuming the LLM response is directly the JSON string
    json_output = response.choices[0].message.content
    return json.loads(json_output)

