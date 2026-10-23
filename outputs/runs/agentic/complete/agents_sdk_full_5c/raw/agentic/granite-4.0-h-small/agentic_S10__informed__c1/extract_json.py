import os
import openai
from model_client import get_openai_api_key

def extract_json(text: str, model_id: str = "gpt-4o-mini") -> dict:
    """Extract structured JSON from text using OpenAI GPT model.

    Args:
        text: Input text from which to extract JSON.
        model_id: OpenAI model family identifier.
    """
    openai.api_key = get_openai_api_key()
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[{"role": "user", "content": f"Parse the following text and output ONLY valid JSON:", "content": text}],
        temperature=0,
    )
    return json.loads(response.choices[0].message.content.strip())

if __name__ == "__main__":
    sample = "User visited Paris, stayed 3 nights, spent 2000 USD, liked the Eiffel Tower."
    print(extract_json(sample))
