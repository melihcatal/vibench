import os
from model_client import LLMClient

def extract_json(text: str) -> dict:
    """Extract structured JSON data from unstructured text using a hosted LLM.

    Args:
        text: The source text containing JSON-like information.
    
    Returns:
        A Python dict representing the extracted JSON.
    """
    client = LLMClient(model="gpt-4")  # OpenAI provider signal
    prompt = f"Parse the following text and return ONLY a JSON object (no other text):\n\n{text}"
    response = client.chat_completion(prompt=prompt)
    json_str = response['choices'][0]['message']['content'].strip()
    return json.loads(json_str)